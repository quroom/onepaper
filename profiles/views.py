from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from profiles.forms import CustomUserForm
from profiles.models import AllowedUser, CustomUser, ExpertProfile, Profile
from profiles.serializers import CustomUserSerializer, ProfileSerializer, ExpertProfileSerializer, AllowedUserSerializer, AllowedProfileListSerializer
from profiles.permissions import IsOwner, IsProfileUserOrReadonly

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

class CurrentProfileViewset(ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = ProfileSerializer
    
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AllowedUserDetail(APIView):
    permission_classes = [IsAuthenticated, IsProfileUserOrReadonly]
    serializer_class = AllowedUserSerializer
    lookup_field = "pk"
    
    def get_object(self, pk):
        obj = get_object_or_404(AllowedUser, profile=pk)
        return obj    

    def get(self, request, pk):
        allowedUser = self.get_object(pk)
        serializer = AllowedUserSerializer(allowedUser)
        return Response(serializer.data)

    def post(self, request, pk):
        allowedUser = get_object_or_404(AllowedUser, profile=pk)
        user = CustomUser.objects.filter(username=request.data['allowed_users']['username'])
        user_by_name = user.filter(name=request.data['allowed_users']['name'])
        if user.count() == 0:
            return Response(ValidationError(_("일치하는 회원 아이디가 없습니다.")), status=status.HTTP_400_BAD_REQUEST)
        if user_by_name.count() == 0:
            return Response(ValidationError(_("이름이 일치하지 않습니다.")), status=status.HTTP_400_BAD_REQUEST)

        allowedUser.allowed_users.add(*user)
        allowedUser.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(allowedUser, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        allowedUser = get_object_or_404(AllowedUser, profile=pk)
        user_list = CustomUser.objects.filter(username__in=request.data['allowed_users'])
        if user_list.count() == 0:
            return Response(ValidationError(_("일치하는 회원이 없습니다.")), status=status.HTTP_400_BAD_REQUEST)

        allowedUser.allowed_users.remove(*user_list)
        allowedUser.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(allowedUser, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

class AllowedProfileList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.filter(allowed_user__allowed_users=request.user, expert_profile=None)
        self_profile = Profile.objects.filter(user=self.request.user, expert_profile=None)
        serializer = ProfileSerializer(profiles | self_profile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
