from rest_framework import serializers
from papers.models import Paper

class PaperSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Paper
        fields = '__all__'