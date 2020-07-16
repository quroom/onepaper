from rest_framework.viewsets import ModelViewSet
from papers.models import Paper
from papers.serializers import PaperSerializer


class PaperViewset(ModelViewSet):    
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)