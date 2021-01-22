import datetime
from rest_framework import serializers
from helps.models import Manual, Notice
from onepaper.serializers import ReadOnlyModelSerializer

class ManualListSerializer(ReadOnlyModelSerializer):
    author = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Manual
        fields = ("id", "parent", "author", "updated_at", "title")

    def get_author(self, instance):
        return instance.author.username

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

class ManualSeiralizer(ReadOnlyModelSerializer):
    author = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Manual
        fields = "__all__"

    def get_author(self, instance):
        return instance.author.username

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

class NoticeListSerializer(ReadOnlyModelSerializer):
    author = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = ("id", "author", "created_at", "updated_at", "title")

    def get_author(self, instance):
        return instance.author.username

    def get_created_at(self, instance):
        return (instance.created_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

class NoticeSeiralizer(ReadOnlyModelSerializer):
    author = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = "__all__"

    def get_author(self, instance):
        return instance.author.username

    def get_created_at(self, instance):
        return (instance.created_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")