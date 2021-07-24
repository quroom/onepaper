import re
import datetime
from django.utils import timezone
from rest_framework import serializers
from helps.models import Notice
from onepaper.serializers import ReadOnlyModelSerializer

class NoticeListSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Notice
        fields = ("id", "created_at", "updated_at", "title", "body", 'is_pinned')

class NoticeSeiralizer(ReadOnlyModelSerializer):
    class Meta:
        model = Notice
        fields = ("id", "created_at", "updated_at", "title", "body", 'is_pinned')