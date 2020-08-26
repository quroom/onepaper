from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from profiles.models import CustomUser, Expert, Profile
from profiles.serializers import CustomUserSerializer, BaseProfileSerializer, ExpertProfileSerializer, GeneralProfileSerializer
from profiles.permissions import IsOwner


class CustomUserViewset(ModelViewSet):
    model = CustomUser
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CurrentProfileViewset(ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = GeneralProfileSerializer

    def list(self, request, *args, **kwargs):
        queryset = Profile.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        expert = getattr(request.user, 'expert', None)

        serializer = GeneralProfileSerializer(queryset, many=True)

        if page is not None:
            if expert is not None:
                serializer = ExpertProfileSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        if expert is not None:
                serializer = ExpertProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        expert = getattr(request.user, 'expert', None)
        if expert is None:
            serializer = self.get_serializer(instance)
        else:
            serializer = ExpertProfileSerializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if serializer.validated_data['authorization_users'] is None:
            serializer.validated_data['authorization_users'] = [
                self.request.user]
        else:
            serializer.validated_data['authorization_users'].append(
                self.request.user)
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if getattr(instance, 'profile_signatues', None) is None:
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def perform_update(self, serializer):
        if serializer.validated_data['authorization_users'] is None:
            serializer.validated_data['authorization_users'] = [
                self.request.user]
        else:
            serializer.validated_data['authorization_users'].append(
                self.request.user)
        serializer.save()


class AuthedProfileList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = request.user.auth_profiles.all()
        serializer = GeneralProfileSerializer(queryset, many=True)
        return Response(serializer.data)
