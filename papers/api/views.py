from rest_framework.viewsets import ModelViewSet
from papers.models import Paper
from papers.api.serializers import PaperSerializer

class PaperViewset(ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer    
