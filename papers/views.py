from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from papers.models import Paper, Contractor, Signature
from papers.serializers import PaperSerializer, SignatureSerializer
from papers.permissions import IsAuthor, IsAuthorOrParticiations, IsParticiations, IsSignatureUser

class HidePaperApiView(APIView):
    def post(self, request, pk):
        paper = get_object_or_404(Paper, pk=pk)
        if paper.status == Paper.DONE:
            signatures = Signature.objects.filter(paper=paper)
            signature = signatures.get(
                user=self.request.user) if signatures.exists() else None
            if signature is None:
                raise ValidationError(_("서명이 되지 않은 계약서는 숨길 수 없습니다."))
            else:
                signature.is_paper_visible = not signature.is_paper_visible
                signature.save()
        else:
            raise ValidationError(_("완료되지 않은 계약서는 숨길 수 없으며, 삭제만 가능합니다."))

class PaperViewset(ModelViewSet):
    queryset = Paper.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrParticiations]
    serializer_class = PaperSerializer

    def list(self, request, *args, **kwargs):
        # queryset = Paper.objects.filter(expert__user=self.request.user)
        # FIX: Call list function by each user type like expert, seller, buyer filter.
        queryset = Paper.objects.filter(paper_contractors__profile__user=self.request.user)
        # queryset = Contractor.objects.select_related('paper').filter(profile__user=self.request.user)
        # queryset = Paper.objects.filter(Q(author=self.request.user) | Q(expert__user=self.request.user) |
        #                             Q(seller__user=self.request.user) | Q(buyer__user=self.request.user)).distinct().order_by('-updated_at')
        serializer_context = {"request": request}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        paper = serializer.save(author=self.request.user)
        instance = self.request.data
        expert = instance.get('expert')
        seller = instance.get('seller')
        buyer = instance.get('buyer')

        if expert != None:
            Contractor.objects.create(paper=paper, profile_id=expert, group=Contractor.EXPERT)
        if seller != None:
            Contractor.objects.create(paper=paper, profile_id=seller, group=Contractor.SELLER)
        if buyer != None:
            Contractor.objects.create(paper=paper, profile_id=buyer, group=Contractor.BUYER)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['update', "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthor()]
        return super(PaperViewset, self).get_permissions()

    def destroy(self, request, *args, **kwargs):
        # FIX: Make destory function works well.
        instance = self.get_object()
        if instance.status == Paper.DRAFT:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise ValidationError(_("완료된 계약서는 삭제할 수 없습니다."))

class SignatureListApiView(generics.ListAPIView):
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated, IsParticiations]

    def get_queryset(self):
        kwarg_id = self.kwargs.get("id")
        return Signature.objects.filter(paper=kwarg_id)

class SignatureCreateApiView(generics.CreateAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated, IsParticiations]

    def perform_create(self, serializer):
        id = self.kwargs.get("id")
        request_user = self.request.user
        paper = get_object_or_404(Paper, id=id)

        if paper.status == Paper.DONE:
            raise ValidationError(_("계약서 작성이 완료되어 서명을 추가할 수 없습니다."))

        signatures = Signature.objects.filter(paper=paper, user=self.request.user)

        if signatures.exists():
            signature = signatures.first()
            if signature.updated_at > paper.updated_at:
                raise serializers.ValidationError(_("이미 서명이 등록되어있습니다."))

        serializer.save(paper=paper, user=self.request.user, image=self.request.data['image'])
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
            raise ValidationError(_("계약서 검토가 완료되어 서명을 수정할 수 없습니다."))

        signatures = Signature.objects.filter(paper=paper, user=self.request.user)
        if not signatures.exists():
            raise ValidationError(_("수정할 수 있는 서명이 없습니다"))

        serializer.save(paper=paper, user=self.request.user)
        return Response(serializer.data)