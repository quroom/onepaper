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

    def get_serializer_class(self):
        expert = getattr(self.request.user, 'expert', None)
        if expert is not None:
            return ExpertProfileSerializer
        else:
            return GeneralProfileSerializer

    def list(self, request, *args, **kwargs):
        queryset = Profile.objects.filter(user=request.user)
        serializer = self.get_serializer_class()(queryset, many=True)
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
        queryset = request.user.auth_profiles.filter(user__expert__isnull=True)
        serializer = GeneralProfileSerializer(queryset, many=True)
        return Response(serializer.data)
