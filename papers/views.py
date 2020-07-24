from rest_framework.response import Response
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from papers.models import Paper
from papers.serializers import PaperSerializer
from papers.permissions import IsAuthor, Disable

class PaperViewset(ModelViewSet):    
    queryset = Paper.objects.all()
    permission_classes = [IsAuthor]
    serializer_class = PaperSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_anonymous == True
            kwargs['password'] == instance.password
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        # queryset = Paper.objects.filter(expert__user=self.request.user)
        # FIX: Call list function by each user type like expert, seller, buyer filter.
        queryset = Paper.objects.filter(Q(author=self.request.user) | Q(expert__user=self.request.user) | Q(seller__user=self.request.user) | Q(buyer__user=self.request.user)).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)