from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics, status, serializers
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from papers.models import Paper, Contractor, Signature
from papers.serializers import PaperSerializer, PaperListSerializer, PaperReadonlySerializer,SignatureSerializer
from papers.permissions import IsAuthor, IsAuthorOrParticiations, IsParticiations, IsSignatureUser

class HidePaperApiView(APIView):
    def post(self, request, pk):
        paper = get_object_or_404(Paper, pk=pk)
        if paper.status == Paper.DONE:
            signatures = Signature.objects.filter(paper=paper)
            signature = signatures.get(
                user=self.request.user) if signatures.exists() else None
            if signature is None:
                return Response(ValidationError(_("서명이 되지 않은 계약서는 숨길 수 없습니다.")), status=status.HTTP_400_BAD_REQUEST)
            else:
                signature.is_paper_visible = not signature.is_paper_visible
                signature.save()
        else:
            return Response(ValidationError(_("완료되지 않은 계약서는 숨길 수 없으며, 삭제만 가능합니다.")), status=status.HTTP_400_BAD_REQUEST)

class PaperListApiView(generics.ListAPIView):
    serializer_class = PaperListSerializer
    permission_classes = [IsAuthenticated, IsParticiations]

    def get_queryset(self):
        return Paper.objects.filter(paper_contractors__profile__user=self.request.user)

class PaperViewset(ModelViewSet):
    queryset = Paper.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrParticiations]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PaperReadonlySerializer
        else:
            return PaperSerializer

    def get_permissions(self):
        if self.action in ['update', "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthor()]
        return super(PaperViewset, self).get_permissions()

    def list(self, request, *args, **kwargs):
        group = getattr(kwargs, 'group', None)
        if group is None:
            queryset = Paper.objects.filter(paper_contractors__profile__user=self.request.user)
        else:
            queryset = Paper.objects.filter(paper_contractors__profile__user=self.request.user, paper_contractors__group=kwargs['group'])

        serializer_context = {"request": request}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

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

    def destroy(self, request, *args, **kwargs):
        # FIX: Make destory function works well.
        instance = self.get_object()
        if instance.status == Paper.DRAFT:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(ValidationError(_("완료된 계약서는 삭제할 수 없습니다.")), status=status.HTTP_400_BAD_REQUEST)
    def validate(self, attrs):
        field1 = attrs.get('field1', self.object.field1)
        field2 = attrs.get('field2', self.object.field2)

        try:
            obj = Model.objects.get(field1=field1, field2=field2)
        except StateWithholdingForm.DoesNotExist:
            return attrs
        if self.object and obj.id == self.object.id:
            return attrs
        else:
            raise serializers.ValidationError('field1 with field2 already exists')
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

        if paper.status == Paper.DONE:
            return Response(ValidationError(_("계약서 작성이 완료되어 서명을 추가할 수 없습니다.")), status=status.HTTP_400_BAD_REQUEST)
            

        signatures = Signature.objects.filter(contractor=contractor)

        if signatures.exists():
            signature = signatures.first()
            if signature.updated_at > paper.updated_at:
                return Response(ValidationError(_("이미 서명이 등록되어있습니다.")), status=status.HTTP_400_BAD_REQUEST)

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
        id = self.kwargs.get("id")
        request_user = self.request.user
        paper = get_object_or_404(Paper, id=id)

        if paper.status == Paper.CONFIRMED:
            Response(ValidationError(_("계약서 검토가 완료되어 서명을 수정할 수 없습니다.")), status=status.HTTP_400_BAD_REQUEST)

        signatures = Signature.objects.filter(paper=paper, user=self.request.user)
        if not signatures.exists():
            Response(ValidationError(_("수정할 수 있는 서명이 없습니다")), status=status.HTTP_400_BAD_REQUEST)

        serializer.save(paper=paper, user=self.request.user)
        return Response(serializer.data)