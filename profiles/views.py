from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from profiles.models import CustomUser, Profile
from profiles.serializers import CustomUserSerializer, ProfileUnauthorizationSerializer, ExpertProfileSerializer, ProfileSerializer
from profiles.permissions import IsOwner

class CustomUserViewset(ModelViewSet):
    model = CustomUser
    serializer_class = CustomUserSerializer
    
    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ProfileViewset(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = Profile.objects.filter(user=request.user)
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if instance.used_count==0:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get_permissions(self):
        if self.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            instance = self.get_object()
            if instance.user.is_expert == True:
                return [IsAuthenticated(), ExpertProfileSerializer()]
        return super(ProfileViewset).get_permissions()