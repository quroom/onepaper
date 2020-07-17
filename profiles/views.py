from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from profiles.models import Expert, Profile
from profiles.serializers import ExpertSerializer, ProfileSerializer
from profiles.permissions import IsOwnerExpert, IsOwnerProfile

class ExpertCreateAPIView(generics.CreateAPIView):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [IsAuthenticated, IsOwnerExpert]

    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(profile=profile)

class ExpertRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Provide *RUD functionality for an answer instance to it's author."""
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [IsAuthenticated, IsOwnerExpert]
    
    def destroy(self, request, *args, **kwargs):
        return HttpResponse('Unauthroized Delete Error')

class ProfileViewset(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfile]

class CurrentProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)