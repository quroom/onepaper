from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from profiles.forms import CustomUserForm
from profiles.models import AuthedUser, CustomUser, ExpertProfile, Profile
from profiles.serializers import CustomUserSerializer, ProfileSerializer, ExpertProfileSerializer, AuthedUserSerializer, AllowedProfileListSerializer
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

class AuthedUserDetail(APIView):
    permission_classes = [IsAuthenticated, IsProfileUserOrReadonly]
    serializer_class = AuthedUserSerializer
    
    def get_object(self, pk):
        obj = get_object_or_404(AuthedUser, profile=pk)
        return obj    

    def get(self, request, pk):
        authedUser = self.get_object(pk)
        serializer = AuthedUserSerializer(authedUser)
        return Response(serializer.data)

    def post(self, request, pk):
        authedUser = get_object_or_404(AuthedUser, profile=pk)
        authedUser.authed_users.add(*request.data['authed_users'])
        authedUser.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(authedUser, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        authedUser = get_object_or_404(AuthedUser, profile=pk)
        authedUser.authed_users.remove(*request.data['authed_users'])
        authedUser.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(authedUser, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

class AllowedProfileList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.filter(authed_user__authed_users=request.user, expert_profile=None)
        # profiles = AuthedUser.objects.filter(authed_users=request.user, profile__expert_profile=None).values('profile')
        # serializer = AllowedProfileListSerializer(authed_users, many=True)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
