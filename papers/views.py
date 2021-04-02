import datetime
import django_filters
from django.db import IntegrityError
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import mixins, generics, status, serializers
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from papers.models import Paper, PaperStatus, Contractor, Signature, ExplanationSignature
from papers.serializers import PaperSerializer, PaperEveryoneSerializer, PaperListSerializer, PaperLoadSerializer, PaperReadonlySerializer, PaperUnalloweUserSerializer, SignatureSerializer, ExplanationSignatureSerializer
from papers.permissions import IsAuthor, IsAuthorOrReadonly, IsContractorUser, IsSignatureUser

class AllowPaperAPIView(APIView):
    permission_classes = [IsAuthenticated, IsContractorUser]

    def get(self, request, pk):
        contractor = get_object_or_404(Contractor.objects.select_related('paper'), pk=pk)
        if contractor.is_allowed == True:
            return Response({"detail": ValidationError(_("이미 계약서 작성이 허용 되었습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.check_object_permissions(self.request, contractor)
            contractor.is_allowed = True
            contractor.save()
        if contractor.paper.status.status == PaperStatus.DRAFT:
            serializer = PaperReadonlySerializer(contractor.paper)
        else:
            serializer = PaperUnalloweUserSerializer(contractor.paper)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExplanationSignatureCreateApiView(generics.CreateAPIView):
    queryset = ExplanationSignature.objects.all()
    serializer_class = ExplanationSignatureSerializer
    permission_classes = [IsAuthenticated, IsContractorUser]

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get("id")
        request_user = self.request.user
        paper = get_object_or_404(Paper, id=id)
        contractor = get_object_or_404(Contractor, id=self.request.data["contractor"])
        self.check_object_permissions(self.request, contractor)

        if paper.status.status == PaperStatus.DONE:
            return Response({"detail": ValidationError(_("계약서 작성이 완료되어 서명을 추가할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        explanation_signatures = ExplanationSignature.objects.filter(contractor=contractor)

        if explanation_signatures.exists():
            explanation_signature = explanation_signatures.first()
            if explanation_signature.updated_at >= paper.updated_at:
                return Response({"detail": ValidationError(_("이미 서명이 등록되어있습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)


class ExplanationSignatureUpdateApiView(mixins.RetrieveModelMixin,
                                        mixins.UpdateModelMixin,
                                        generics.GenericAPIView):
    queryset = ExplanationSignature.objects.all()
    serializer_class = ExplanationSignatureSerializer
    permission_classes = [IsAuthenticated, IsSignatureUser]

    def put(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        explanation_signature = get_object_or_404(ExplanationSignature, id=id)

        if explanation_signature.contractor.paper.status.status == PaperStatus.DONE:
            return Response({"detail": ValidationError(_("완료된 계약서의 서명은 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(request, *args, **kwargs)

class HidePaperApiView(APIView):
    permission_classes = [IsAuthenticated, IsContractorUser]

    def post(self, request, pk):
        contractor = get_object_or_404(Contractor, paper=pk, profile__user=self.request.user)
        try:
            if contractor.paper.status.status == PaperStatus.DONE:
                if contractor.signature:
                    self.check_object_permissions(self.request, contractor)
                    contractor.is_paper_hidden = not contractor.is_paper_hidden
                    contractor.save()
            else:
                return Response({"detail": ValidationError(_("완료되지 않은 계약서는 숨길 수 없으며, 삭제만 가능합니다."))}, status=status.HTTP_400_BAD_REQUEST)
        except papers.models.Contractor.signature.RelatedObjectDoesNotExist:
            return Response({"detail": ValidationError(_("서명이 되지 않은 계약서는 숨길 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        papers = Paper.objects.filter(paper_contractors__profile__user=self.request.user, paper_contractors__is_paper_hidden=True)
        serializer = PaperListSerializer(papers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllPaperList(APIView, PageNumberPagination):
    def get(self, request, format=None):
        bjdong = self.request.query_params.get("bjdong")
        if not bjdong:
            papers = Paper.objects.filter(status__status=PaperStatus.DONE)
        else:
            bjdong = bjdong.strip()
            papers = Paper.objects.filter(status__status=PaperStatus.DONE, address__bjdongName__icontains=bjdong)
        page = self.paginate_queryset(papers, request, view=self)
        serializer = PaperEveryoneSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class PaperLoadAPIView(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaperLoadSerializer

    def get_queryset(self):
        return Paper.objects.filter(paper_contractors__profile__user=self.request.user).select_related('author', 'address', 'status')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class PaperFilter(django_filters.FilterSet):
    status = django_filters.NumberFilter(field_name="status__status")
    group = django_filters.NumberFilter(field_name="paper_contractors__group")
    old_address = django_filters.CharFilter(lookup_expr='icontains', field_name='address__old_address')
    dong = django_filters.CharFilter(field_name='address__dong')
    ho = django_filters.CharFilter(field_name='address__ho')

    class Meta:
        model = Paper
        fields = ['status', 'paper_contractors', 'address']

class PaperViewset(ModelViewSet):
    __basic_fields = ('status', 'group', 'old_address', 'dong', 'ho', 'to_date')
    permission_classes = [IsAuthenticated, IsAuthorOrReadonly]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filter_fields = __basic_fields
    filter_class = PaperFilter

    def get_queryset(self):
        return Paper.objects.filter(paper_contractors__profile__user=self.request.user).select_related('author', 'address', 'status').prefetch_related('paper_contractors')

    def get_object(self):
        obj = get_object_or_404(Paper.objects.select_related('author', 'address', 'status').prefetch_related('paper_contractors', 'paper_contractors__profile', 'paper_contractors__profile__user', 'paper_contractors__profile__expert_profile'), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.action == 'list':
            return PaperListSerializer
        elif self.request.method in SAFE_METHODS:
            return PaperReadonlySerializer
        else:
            return PaperSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not Contractor.objects.filter(paper=instance, profile__user=self.request.user).exists():
            serializer = PaperEveryoneSerializer(instance)
        elif Contractor.objects.filter(paper=instance, is_allowed=False).exists():
            serializer = PaperUnalloweUserSerializer(instance)
        else:
            serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        paper = serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        if instance.status.status == PaperStatus.DONE:
            return Response({"detail": ValidationError(_("완료된 계약서는 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        elif instance.status.status == PaperStatus.PROGRESS:
            initial_date = datetime.datetime(1,1,1)
            signature_first_updated_at = getattr(Signature.objects.order_by('updated_at').filter(contractor__paper=instance).first(), 'updated_at', datetime.datetime(1,1,1))
            #Reset tzinfo. If there is not this code, we will get 'can't compare offset-naive and offset-aware datetimes' error.
            signature_first_updated_at = signature_first_updated_at.replace(tzinfo=None)
            explanation_signature_first_updated_at = getattr(ExplanationSignature.objects.order_by('updated_at').filter(contractor__paper=instance).first(), 'updated_at', datetime.datetime(1,1,1))
            explanation_signature_first_updated_at = explanation_signature_first_updated_at.replace(tzinfo=None)
            first_signature_time = signature_first_updated_at if signature_first_updated_at <= explanation_signature_first_updated_at else explanation_signature_first_updated_at
            if first_signature_time != initial_date:
                if (datetime.datetime.utcnow() - first_signature_time).total_seconds() / 3600 > 12:
                    return Response({"detail": ValidationError(_("최초 서명 후 12시간이 지나면 계약서를 수정 할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

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
            initial_date = datetime.datetime(1,1,1)
            signature_first_updated_at = getattr(Signature.objects.order_by('updated_at').filter(contractor__paper=instance).first(), 'updated_at', datetime.datetime(1,1,1))
            #Reset tzinfo. If there is not this code, we will get 'can't compare offset-naive and offset-aware datetimes' error.
            signature_first_updated_at = signature_first_updated_at.replace(tzinfo=None)
            explanation_signature_first_updated_at = getattr(ExplanationSignature.objects.order_by('updated_at').filter(contractor__paper=instance).first(), 'updated_at', datetime.datetime(1,1,1))
            explanation_signature_first_updated_at = explanation_signature_first_updated_at.replace(tzinfo=None)
            first_signature_time = signature_first_updated_at if signature_first_updated_at <= explanation_signature_first_updated_at else explanation_signature_first_updated_at
            if first_signature_time != initial_date:
                if (datetime.datetime.utcnow() - first_signature_time).total_seconds() / 3600 > 12:
                        return Response({"detail": ValidationError(_("최초 서명 후 12시간이 지나면 계약서를 삭제 할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SignatureCreateApiView(generics.CreateAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated, IsContractorUser]

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get("id")
        request_user = self.request.user
        paper = get_object_or_404(Paper, id=id)
        contractor = get_object_or_404(Contractor, id=self.request.data["contractor"])
        self.check_object_permissions(self.request, contractor)
        if paper.status.status == PaperStatus.DONE:
            return Response({"detail": ValidationError(_("계약서 작성이 완료되어 서명을 추가할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        signatures = Signature.objects.filter(contractor=contractor)

        if signatures.exists():
            signature = signatures.first()
            if signature.updated_at >= paper.updated_at:
                return Response({"detail": ValidationError(_("이미 서명이 등록되어있습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)

class SignatureUpdateApiView(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             generics.GenericAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated, IsSignatureUser]

    def put(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        signature = get_object_or_404(Signature, id=id)
        if signature.contractor.paper.status.status == PaperStatus.DONE:
            return Response({"detail": ValidationError(_("완료된 계약서의 서명은 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(request, *args, **kwargs)