from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics, status
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from profiles.forms import CustomUserForm
from papers.models import Contractor
from profiles.models import AllowedUser, CustomUser, ExpertProfile, Profile, Mandate
from profiles.serializers import AllowedUserSerializer, AllowedProfileListSerializer, ApproveExpertSerializer, CustomUserIDNameSerializer, CustomUserSerializer, ExpertProfileSerializer, MandateSerializer, MandateReadOnlySerializer, ProfileSerializer, ProfileBasicInfoSerializer
from profiles.permissions import IsAdmin, IsAuthorOrDesignator, IsOwnerOrReadonly, IsOwner, IsProfileUserOrReadonly

class CustomUserViewset(ModelViewSet):
    model = CustomUser
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

#FIXME Implment in frontend. 
class HideProfileApiView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    def post(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            profile.is_visible = not profile.is_visible
            profile.save()
        except Profile.DoesNotExist:
            return Response({"detail": ValidationError(_("프로필이 존재하지 않습니다."))})
        profiles = Profile.objects.filter(user=self.request.user, is_visible=True)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileDetailAPIView(APIView):
    def get_object(self, pk):
        return Profile.objects.get(pk=pk)
        
    def get(self, request, pk, format=None):
        try:
            profile = self.get_object(pk)
        except Profile.DoesNotExist:
            return Response({"detail": ValidationError(_("프로필이 존재하지 않습니다."))})
        serializer = ProfileBasicInfoSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CurrentProfileViewset(ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_serializer_class(self):
        if self.request.user.request_expert:
            return ExpertProfileSerializer
        else:
            return ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if Contractor.objects.filter(profile=instance).exists():
            return Response(ValidationError(_("작성한 계약서가 있는 경우 프로필을 수정할 수 없습니다.")), status=status.HTTP_400_BAD_REQUEST)

        if Mandate.objects.filter(designator=instance).exists() or Mandate.objects.filter(designee=instance).exists():
            return Response(ValidationError(_("작성한 위임장이 있는 경우 프로필을 수정할 수 없습니다.")), status=status.HTTP_400_BAD_REQUEST)        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Contractor.objects.filter(profile=instance).exists():
            return Response({"detail": ValidationError(_("작성한 계약서가 있는 경우 프로필을 삭제할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        if Mandate.objects.filter(designator=instance).exists() or Mandate.objects.filter(designee=instance).exists():
            return Response({"detail": ValidationError(_("작성한 위임장이 있는 경우 프로필을 삭제할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
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
            return Response({"detail": ValidationError(_("승인 가능한 전문가가 선택되지 않았습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        expert_profiles = ExpertProfile.objects.filter(id__in=request.data['profiles']).exclude(status=ExpertProfile.APPROVED)
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
        expert_profiles = ExpertProfile.objects.filter(id__in=request.data['profiles'])
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

class AllowedUserDetail(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated, IsProfileUserOrReadonly]
    serializer_class = AllowedUserSerializer
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
        user_queryset = CustomUser.objects.filter(username=request.data['allowed_users']['username'])
        if user_queryset.count() == 0:
            return Response({"detail": ValidationError(_("회원 아이디가 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_queryset.get(name=request.data['allowed_users']['name'])
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
        user_list = CustomUser.objects.filter(username__in=request.data['allowed_users'])
        if user_list.count() == 0:
            return Response({"detail": ValidationError(_("일치하는 회원이 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        allowedUser.allowed_users.remove(*user_list)
        allowedUser.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class AllowedProfileList(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.filter(allowed_user__allowed_users=request.user)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        return (Mandate.objects.filter(designator__user=self.request.user) | Mandate.objects.filter(designee__user=self.request.user)).distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        if bool(instance.designator_signature):
            return Response({"detail": ValidationError(_("서명이 완료된 위임장은 수정할 수 없습니다."))}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
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
