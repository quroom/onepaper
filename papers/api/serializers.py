from rest_framework import serializers
from papers.models import Paper

class PaperSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Paper
        fields = '__all__'