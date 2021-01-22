from django.db import transaction
from django.db.models import Exists, Q
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from rest_framework import mixins, generics, status
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from profiles.forms import CustomUserForm
from papers.models import Contractor, Paper
from profiles.models import AllowedUser, CustomUser, ExpertProfile, Profile, Mandate
from profiles.serializers import ApproveExpertSerializer, CustomUserIDNameSerializer, CustomUserSerializer, ExpertProfileSerializer, MandateSerializer, MandateEveryoneSerializer, MandateReadOnlySerializer, ProfileSerializer, ProfileBasicInfoSerializer, ProfileReadonlySerializer
from profiles.permissions import IsAdmin, IsAuthorOrDesignator, IsOwnerOrReadonly, IsOwner, IsProfileUserOrReadonly

class AllowedProfileList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        profiles = Profile.objects.filter(
            allowed_user__allowed_users=request.user).filter(expert_profile=None).filter(is_active=True).select_related('user')
        serializer = ProfileReadonlySerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllowedUserDetail(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated, IsProfileUserOrReadonly]
    lookup_field = "pk"

    def get_object(self, pk):
        obj = get_object_or_404(AllowedUser, profile=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        allowedUser = self.get_object(pk)
        allowed_users = allowedUser.allowed_users.exclude(id=request.user.id)
        page = self.paginate_queryset(allowed_users, request, view=self)
        serializer = CustomUserIDNameSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, pk):
        allowedUser = self.get_object(pk)

        if request.data['allowed_users']['username'] == request.user.username:
            return Response({"detail": ValidationError(_("자기 자신의 아이디는 추가할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        user_queryset = CustomUser.objects.filter(
            username=request.data['allowed_users']['username'])
        if user_queryset.count() == 0:
            return Response({"detail": ValidationError(_("회원 아이디가 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_queryset.get(
                name=request.data['allowed_users']['name'])
        except CustomUser.DoesNotExist:
            return Response({"detail": ValidationError(_("이름이 일치하지 않습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        if user in allowedUser.allowed_users.all():
            return Response({"detail": ValidationError(_("이미 추가된 회원입니다."))}, status=status.HTTP_400_BAD_REQUEST)

        allowedUser.allowed_users.add(user)
        allowedUser.save()

        allowed_users = allowedUser.allowed_users.exclude(id=request.user.id)
        page = self.paginate_queryset(allowed_users, request, view=self)
        serializer = CustomUserIDNameSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def delete(self, request, pk):
        allowedUser = self.get_object(pk)

        if request.user.username in request.data['allowed_users']:
            return Response({"detail": ValidationError(_("자신의 아이디는 삭제할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        user_list = allowedUser.allowed_users.filter(username__in=request.data['allowed_users'])

        if user_list.count() != len(request.data['allowed_users']):
            return Response({"detail": ValidationError(_("빠른거래 리스트에 추가되지 않은 회원은 삭제 할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        response = allowedUser.allowed_users.remove(*user_list)
        response = allowedUser.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ApproveExpert(mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = ExpertProfile.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ApproveExpertSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if len(request.data['profiles']) == 0:
            return Response({"detail": ValidationError(_("전문가가 선택되지 않았습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        expert_profiles = ExpertProfile.objects.filter(
            id__in=request.data['profiles']).exclude(status=ExpertProfile.APPROVED)
        if expert_profiles.exists() is False:
            return Response({"detail": ValidationError(_("승인 가능한 전문가가 선택되지 않았습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        expert_profiles.update(status=ExpertProfile.APPROVED)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def delete(self, request):
        expert_profiles = ExpertProfile.objects.filter(
            id__in=request.data['profiles'])
        if expert_profiles.exists() is False:
            return Response({"detail": ValidationError(_("전문가가 선택되지 않았습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        expert_profiles.update(status=ExpertProfile.DENIED)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

class ExpertProfileList(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    def get(self, request):
        queryset = Profile.objects.filter(user=self.request.user, expert_profile__status=ExpertProfile.APPROVED).select_related('user', 'address', 'expert_profile')
        serializer = ProfileReadonlySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.request.user.is_expert:
            return Profile.objects.filter(user=self.request.user).select_related('user', 'address')
        else:
            return Profile.objects.filter(user=self.request.user).select_related('user', 'address', 'expert_profile')

    def get_serializer_class(self):
        if self.request.user.is_expert:
            return ExpertProfileSerializer
        else:
            return ProfileSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        expert_profile = getattr(instance, 'expert_profile', None)
        if not expert_profile is None:
            if expert_profile.status != ExpertProfile.REQUEST and expert_profile.status != ExpertProfile.DENIED :
                return Response({"detail": ValidationError(_("승인된 전문가 프로필은 수정 할 수 없습니다. 새 프로필을 만드세요."))}, status=status.HTTP_400_BAD_REQUEST)
               
        if Contractor.objects.filter(profile=instance).exists():
            return Response({"detail": ValidationError(_("거래 계약서가 있는 경우 프로필을 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        if Mandate.objects.filter(designator=instance).exists() or Mandate.objects.filter(designee=instance).exists():
            return Response({"detail": ValidationError(_("작성한 위임장이 있는 경우 프로필을 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    @transaction.atomic
    def perform_create(self, serializer):
        Profile.objects.filter(user=self.request.user).update(is_active=False)
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Contractor.objects.filter(profile=instance).exists():
            return Response({"detail": ValidationError(_("거래 계약서가 있는 경우 프로필을 삭제할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        if Mandate.objects.filter(designator=instance).exists() or Mandate.objects.filter(designee=instance).exists():
            return Response({"detail": ValidationError(_("작성한 위임장이 있는 경우 프로필을 삭제할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomUserViewset(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    permission_classes = [IsAuthenticated]
    model = CustomUser
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if Paper.objects.filter(paper_contractors__profile__user=instance).exists():
            return Response({"detail": ValidationError(_("계약서가 존재하는 경우 회원 정보를 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            if not (instance.username == request.data['username'] and instance.email == request.data['email'] and instance.name == request.data['name']):
                return Response({"detail": ValidationError(_("입력하신 정보가 현재 회원의 정보와 일치하지 않습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"detail": ValidationError(_("탈퇴할 회원의 정보를 모두 입력해주세요."))}, status=status.HTTP_400_BAD_REQUEST)
        if Paper.objects.filter(paper_contractors__profile__user=instance).exists():
            instance.is_active = False
            instance.save()
            return Response({"user_delete": _("탈퇴처리 되었습니다.")}, status=status.HTTP_200_OK)
        else:
            instance.delete()
            return Response({"user_delete": _("탈퇴처리 되었습니다. 계정정보 또한 완전히 삭제되었습니다.")}, status=status.HTTP_200_OK)

class MandateViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthorOrDesignator()]
        return super(MandateViewset, self).get_permissions()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MandateReadOnlySerializer
        else:
            return MandateSerializer

    def get_queryset(self):
        mandates = Mandate.objects.all().select_related('address', 'designator', 'designator__address', 'designator__user', 'designee', 'designee__address', 'designee__user', 'author').prefetch_related('designator__expert_profile', 'designee__expert_profile')
        return (mandates.filter(designator__user=self.request.user) | mandates.filter(designee__user=self.request.user)).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Mandate, pk=self.kwargs.get("pk"))
        if(instance.designator.user != self.request.user and instance.designee.user != self.request.user):
            serializer = MandateEveryoneSerializer(instance)
        else:
            serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        if bool(instance.designator_signature):
            return Response({"detail": ValidationError(_("서명이 완료된 위임장은 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if bool(instance.designator_signature):
            return Response({"detail": ValidationError(_("서명이 완료된 위임장은 삭제할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class OpenProfileList(APIView, PageNumberPagination):
    def get(self, request, format=None):
        name = self.request.query_params.get("name")
        mobile_number = self.request.query_params.get("mobile_number")

        if name == '' or mobile_number == '':
            return Response({"detail": ValidationError(_("성함, 연락처 모두 입력해야 합니다."))}, status=status.HTTP_400_BAD_REQUEST)

        profiles = Profile.objects.filter(user__name=name, mobile_number=mobile_number, is_active=True)
        page = self.paginate_queryset(profiles, request, view=self)
        serializer = ProfileBasicInfoSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class OpenProfileDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileBasicInfoSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

# FIXME Implment in frontend.
class SetDefaultProfile(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        self.check_object_permissions(self.request, profile)
        profiles = Profile.objects.filter(user=self.request.user)
        active_profiles = profiles.filter(is_active=True)
        with transaction.atomic():
            active_profiles.update(is_active=False)
            profile.is_active = True
            profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)