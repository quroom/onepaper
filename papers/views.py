import datetime
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, generics, status, serializers
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from papers.models import Paper, PaperStatus, Contractor, Signature
from papers.serializers import PaperSerializer, PaperListSerializer, PaperReadonlySerializer, SignatureSerializer
from papers.permissions import IsAuthor, IsAuthorOrParticiations, IsParticiations, IsSignatureUser

class HidePaperApiView(APIView):
    def post(self, request, pk):
        contractors = Contractor.objects.filter(paper=pk, profile__user=self.request.user)
        if contractors.exists():
            contractor = contractors.first()
            try:
                if contractor.paper.status == PaperStatus.DONE:
                    if contractor.signature:
                        contractor.is_paper_visible = not contractor.is_paper_visible
                        contractor.save()
                else:
                    return Response({"detail": ValidationError(_("완료되지 않은 계약서는 숨길 수 없으며, 삭제만 가능합니다."))}, status=status.HTTP_400_BAD_REQUEST)
            except papers.models.Contractor.signature.RelatedObjectDoesNotExist:
                return Response({"detail": ValidationError(_("서명이 되지 않은 계약서는 숨길 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": ValidationError(_("계약서의 계약자가 아닙니다."))}, status=status.HTTP_400_BAD_REQUEST)

class PaperListApiView(generics.ListAPIView):
    serializer_class = PaperListSerializer
    permission_classes = [IsAuthenticated, IsParticiations]

    def get_queryset(self):
        return Paper.objects.filter(paper_contractors__profile__user=self.request.user)

class PaperViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrParticiations]
    
    def get_queryset(self):
        filters = {}
        for key in self.request.query_params:
            if key=='status':
                filters['status'] = self.request.query_params.get(key)
            elif key=='group':
                filters['paper_contractors__group'] = self.request.query_params.get(key)

        papers = Paper.objects.filter(paper_contractors__profile__user=self.request.user, **filters)
        return papers

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PaperReadonlySerializer
        else:
            return PaperSerializer

    def get_permissions(self):
        if self.action in ['update', "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthor()]
        return super(PaperViewset, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        paper = serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        if instance.status.status == PaperStatus.PROGRESS:
            if (datetime.datetime.now().astimezone() - instance.updated_at).total_seconds() / 3600 > 12:
                return Response({"detail": ValidationError(_("최초 서명 후 12시간이 지나면 계약서를 수정 할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        elif instance.status.status == PaperStatus.DONE:
            return Response({"detail": ValidationError(_("완료된 계약서를 수정 할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # FIX: Make destory function works well.
        instance = self.get_object()
        if instance.status.status == PaperStatus.DONE:
            return Response({"detail": ValidationError(_("완료된 계약서는 삭제할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        elif instance.status.status == PaperStatus.PROGRESS:
            if (datetime.datetime.now().astimezone() - instance.updated_at).total_seconds()/3600 > 12:
                return Response({"detail": ValidationError(_("최초 서명 후 12시간이 지나면 계약서를 수정 할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SignatureListApiView(generics.ListAPIView):
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated, IsParticiations]

    def get_queryset(self):
        kwarg_id = self.kwargs.get("id")
        return Signature.objects.filter(contractor__paper__id=kwarg_id)

class SignatureCreateApiView(generics.CreateAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated, IsParticiations]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_create(self, serializer):
        id = self.kwargs.get("id")
        request_user = self.request.user
        paper = get_object_or_404(Paper, id=id)
        contractor = get_object_or_404(Contractor, id=self.request.data["contractor"])

        if paper.status == PaperStatus.DONE:
            return Response({"detail": ValidationError(_("계약서 작성이 완료되어 서명을 추가할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        signatures = Signature.objects.filter(contractor=contractor)

        if signatures.exists():
            signature = signatures.first()
            if signature.updated_at >= paper.updated_at:
                return Response({"detail": ValidationError(_("이미 서명이 등록되어있습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(contractor=contractor, image=self.request.data['image'])
        return Response(serializer.data)

class SignatureUpdateApiView(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             generics.GenericAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated, IsSignatureUser]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        id = self.kwargs.get("pk")
        signatures = Signature.objects.filter(id=id)
        if not signatures.exists():
            Response({"detail": ValidationError(_("수정할 수 있는 서명이 없습니다"))}, status=status.HTTP_400_BAD_REQUEST)
        
        signature = signatures.first()

        if signature.contractor.paper == PaperStatus.DONE:
            Response({"detail": ValidationError(_("완료된 계약서의 서명은 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(image=self.request.data['image'])
        return Response(serializer.data)