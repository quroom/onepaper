from rest_framework.response import Response
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from papers.models import Paper
from papers.serializers import PaperSerializer
from papers.permissions import IsPartipantOnly

class PaperViewset(ModelViewSet):    
    queryset = Paper.objects.all()
    permission_classes = [IsPartipantOnly]
    serializer_class = PaperSerializer

    def list(self, request, *args, **kwargs):
        queryset = Paper.objects.filter(Q(author=self.request.user) | Q(expert=self.request.user) | Q(seller=self.request.user) | Q(buyer=self.request.user)).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)