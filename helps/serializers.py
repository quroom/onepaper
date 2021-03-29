import re
import datetime
from django.utils import timezone
from rest_framework import serializers
from helps.models import Notice
from onepaper.serializers import ReadOnlyModelSerializer

class NoticeListSerializer(ReadOnlyModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = ("id", "created_at", "updated_at", "title", "body")

    def get_created_at(self, instance):
        return (instance.created_at).strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, instance):
        return timezone.localtime(instance.updated_at).strftime("%Y-%m-%d %H:%M:%S")

class NoticeSeiralizer(ReadOnlyModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = ("id", "created_at", "updated_at", "title", "body")

    def get_created_at(self, instance):
        return (instance.created_at).strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, instance):
        return timezone.localtime(instance.updated_at).strftime("%Y-%m-%d %H:%M:%S")