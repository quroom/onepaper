import datetime
import django_filters
from django.db.models import BooleanField, Case, Exists, OuterRef, Value, When
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
from papers.serializers import PaperSerializer, PaperEveryoneSerializer, PaperEveryoneDetailSerializer, PaperListSerializer, PaperLoadSerializer, PaperReadonlySerializer, PaperUnalloweUserSerializer, PaperUnalloweUserDetailSerializer, SignatureSerializer, ExplanationSignatureSerializer
from papers.permissions import IsAuthor, IsAuthorOrReadonly, IsContractorUser, IsSignatureUser

class PaperFilter(django_filters.FilterSet):
    status = django_filters.NumberFilter(field_name="status__status")
    group = django_filters.NumberFilter(field_name="paper_contractors__group")
    old_address = django_filters.CharFilter(lookup_expr='icontains', field_name='address__old_address')
    dong = django_filters.CharFilter(field_name='address__dong')
    ho = django_filters.CharFilter(field_name='address__ho')

    class Meta:
        model = Paper
        fields = ['status', 'paper_contractors', 'address']

class AllPaperFilter(django_filters.FilterSet):
    status = django_filters.NumberFilter(field_name="status__status")
    bjdong = django_filters.CharFilter(lookup_expr='icontains', field_name='address__bjdongName')

    class Meta:
        model = Paper
        fields = ['status', 'address']

class AllPaperList(generics.ListAPIView):
    serializer_class = PaperEveryoneSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadonly]
    __basic_fields = ('status', 'bjdong')
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = __basic_fields
    filter_class = AllPaperFilter

    def get_queryset(self):
        return Paper.objects.all().annotate(is_contractor=Case(When(Exists(Contractor.objects.filter(paper=OuterRef('pk'), profile__user=self.request.user)), then=True), output_field=BooleanField(), default=Value(False))).select_related('author')

class AllowPaperAPIView(APIView):
    permission_classes = [IsAuthenticated, IsContractorUser]

    def put(self, request, pk):
        contractor = get_object_or_404(Contractor.objects.select_related('paper'), pk=pk)
        self.check_object_permissions(self.request, contractor)
        is_allowed = request.data.get("is_allowed")

        if is_allowed == None:
            return Response({"detail": ValidationError(_("요청 데이터가 올바르지 않습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        if contractor.paper.status.status in (PaperStatus.PROGRESS, PaperStatus.DONE):
            return Response({"detail": ValidationError(_("서명 또는 완료된 계약서는 거절할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if contractor.is_hidden:
                return Response({"detail": ValidationError(_("숨김 처리된 계약서는 승인/거절이 불가합니다. 계약서 보임 처리 후 재요청 해주세요."))}, status=status.HTTP_400_BAD_REQUEST)

            if is_allowed == True:
                if contractor.is_allowed  == True:
                    return Response({"detail": ValidationError(_("이미 계약서 작성이 허용 되었습니다."))}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    contractor.is_allowed = True
                    contractor.save()
            else:
                if contractor.is_allowed == False:
                    return Response({"detail": ValidationError(_("이미 계약서 작성이 거절 되었습니다."))}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    contractor.is_allowed = False
                    contractor.save()


        if contractor.paper.status.status == PaperStatus.DRAFT:
            serializer = PaperReadonlySerializer(contractor.paper, context={'request': request})
        else:
            serializer = PaperUnalloweUserSerializer(contractor.paper)
        return Response(serializer.data, status=status.HTTP_200_OK)

class HidePaperAPIView(APIView):
    permission_classes = [IsAuthenticated, IsContractorUser]

    def put(self, request, pk):
        contractor = get_object_or_404(Contractor.objects.select_related('paper'), pk=pk)
        self.check_object_permissions(self.request, contractor)
        is_hidden = request.data.get("is_hidden")

        if is_hidden == None:
            return Response({"detail": ValidationError(_("요청 데이터가 올바르지 않습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        if contractor.paper.status.status in (PaperStatus.DENIED, PaperStatus.DONE):
            if is_hidden:
                if contractor.is_hidden:
                    return Response({"detail": ValidationError(_("이미 계약서가 숨김 처리 되었습니다."))}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    contractor.is_hidden = True
                    contractor.save()
            else:
                if contractor.is_hidden == False:
                    return Response({"detail": ValidationError(_("이미 계약서가 보임 처리 되었습니다."))}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    contractor.is_hidden = False
                    contractor.save()
        else:
            return Response({"detail": ValidationError(_("완료 또는 거절된 계약서만 숨김 처리가 가능합니다."))}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PaperReadonlySerializer(contractor.paper, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExplanationSignatureCreateAPIView(generics.CreateAPIView):
    queryset = ExplanationSignature.objects.all()
    serializer_class = ExplanationSignatureSerializer
    permission_classes = [IsAuthenticated, IsContractorUser]

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get("id")
        request_user = self.request.user
        paper = get_object_or_404(Paper, id=id)
        contractor = get_object_or_404(Contractor, id=self.request.data["contractor"])
        self.check_object_permissions(self.request, contractor)

        if paper.status.status in (PaperStatus.DONE, PaperStatus.DENIED):
            return Response({"detail": ValidationError(_("완료 또는 거절된 계약서는 서명을 추가할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        explanation_signatures = ExplanationSignature.objects.filter(contractor=contractor)

        if explanation_signatures.exists():
            explanation_signature = explanation_signatures.first()
            if explanation_signature.updated_at >= paper.updated_at:
                return Response({"detail": ValidationError(_("이미 서명이 등록되어있습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)

class ExplanationSignatureUpdateAPIView(mixins.RetrieveModelMixin,
                                        mixins.UpdateModelMixin,
                                        generics.GenericAPIView):
    queryset = ExplanationSignature.objects.all()
    serializer_class = ExplanationSignatureSerializer
    permission_classes = [IsAuthenticated, IsSignatureUser]

    def put(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        explanation_signature = get_object_or_404(ExplanationSignature, id=id)

        if explanation_signature.contractor.paper.status.status in (PaperStatus.DONE, PaperStatus.DENIED):
            return Response({"detail": ValidationError(_("완료 또는 거절된 계약서는 서명을 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(request, *args, **kwargs)

class PaperLoadAPIView(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaperLoadSerializer

    def get_queryset(self):
        return Paper.objects.filter(paper_contractors__profile__user=self.request.user).select_related('author', 'address', 'status')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class PaperViewset(ModelViewSet):
    __basic_fields = ('status', 'group', 'old_address', 'dong', 'ho', 'to_date')
    permission_classes = [IsAuthenticated, IsAuthorOrReadonly]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filter_fields = __basic_fields
    filter_class = PaperFilter

    def get_queryset(self):
        is_hidden = self.request.query_params.get("is_hidden")
        if is_hidden:
            return Paper.objects.filter(paper_contractors__profile__user=self.request.user, paper_contractors__is_hidden=is_hidden).select_related('author', 'address', 'status').prefetch_related('paper_contractors')
        else:
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
            serializer = PaperEveryoneDetailSerializer(instance, context={'request': request} )
        elif Contractor.objects.filter(paper=instance).exclude(is_allowed=True):
            serializer = PaperUnalloweUserDetailSerializer(instance, context={'request': request} )
        else:
            serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        paper = serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        if instance.status.status in (PaperStatus.DONE, PaperStatus.DENIED):
            return Response({"detail": ValidationError(_("완료 또는 거절된 계약서는 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        elif instance.status.status == PaperStatus.PROGRESS:
            initial_date = datetime.datetime(9999,12,31)
            signature_first_updated_at = getattr(Signature.objects.order_by('updated_at').filter(contractor__paper=instance, updated_at__gte=instance.updated_at).first(), 'updated_at', initial_date)
            #Reset tzinfo. If there is not this code, we will get 'can't compare offset-naive and offset-aware datetimes' error.
            signature_first_updated_at = signature_first_updated_at.replace(tzinfo=None)
            explanation_signature_first_updated_at = getattr(ExplanationSignature.objects.order_by('updated_at').filter(contractor__paper=instance, updated_at__gte=instance.updated_at).first(), 'updated_at', initial_date)
            explanation_signature_first_updated_at = explanation_signature_first_updated_at.replace(tzinfo=None)
            first_signature_time = signature_first_updated_at if signature_first_updated_at <= explanation_signature_first_updated_at else explanation_signature_first_updated_at
            if first_signature_time != initial_date:
                if (datetime.datetime.utcnow() - first_signature_time).total_seconds() / 3600 > 24:
                    return Response({"detail": ValidationError(_("최초 서명 후 24시간이 지나면 계약서를 수정 할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

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
            initial_date = datetime.datetime(9999,12,31)
            signature_first_updated_at = getattr(Signature.objects.order_by('updated_at').filter(contractor__paper=instance, updated_at__gte=instance.updated_at).first(), 'updated_at', initial_date)
            #Reset tzinfo. If there is not this code, we will get 'can't compare offset-naive and offset-aware datetimes' error.
            signature_first_updated_at = signature_first_updated_at.replace(tzinfo=None)
            explanation_signature_first_updated_at = getattr(ExplanationSignature.objects.order_by('updated_at').filter(contractor__paper=instance, updated_at__gte=instance.updated_at).first(), 'updated_at', initial_date)
            explanation_signature_first_updated_at = explanation_signature_first_updated_at.replace(tzinfo=None)
            first_signature_time = signature_first_updated_at if signature_first_updated_at <= explanation_signature_first_updated_at else explanation_signature_first_updated_at
            if first_signature_time != initial_date:
                if (datetime.datetime.utcnow() - first_signature_time).total_seconds() / 3600 > 24:
                        return Response({"detail": ValidationError(_("최초 서명 후 24시간이 지나면 계약서를 삭제 할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SignatureCreateAPIView(generics.CreateAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated, IsContractorUser]

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get("id")
        request_user = self.request.user
        paper = get_object_or_404(Paper, id=id)
        contractor = get_object_or_404(Contractor, id=self.request.data["contractor"])
        self.check_object_permissions(self.request, contractor)
        if paper.status.status in (PaperStatus.DONE, PaperStatus.DENIED):
            return Response({"detail": ValidationError(_("완료 또는 거절된 계약서는 서명을 추가할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        signatures = Signature.objects.filter(contractor=contractor)

        if signatures.exists():
            signature = signatures.first()
            if signature.updated_at >= paper.updated_at:
                return Response({"detail": ValidationError(_("이미 서명이 등록되어있습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)

class SignatureUpdateAPIView(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             generics.GenericAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated, IsSignatureUser]

    def put(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        signature = get_object_or_404(Signature, id=id)
        if signature.contractor.paper.status.status in (PaperStatus.DONE, PaperStatus.DENIED):
            return Response({"detail": ValidationError(_("완료 또는 거절된 계약서는 서명을 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(request, *args, **kwargs)