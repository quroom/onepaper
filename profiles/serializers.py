from django.http import JsonResponse
from rest_framework import serializers
from profiles.models import Expert, Profile
import re

class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        exclude = ["profile"]

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    ip_address = serializers.IPAddressField(read_only=True)
    average_response_time = serializers.FloatField(read_only=True)
    response_rate = serializers.FloatField(read_only=True)
    contract_success_rate = serializers.FloatField(read_only=True)
    average_response_time = serializers.FloatField(read_only=True)
    expert = serializers.SerializerMethodField()

    # signature = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

    def get_expert(self, obj):
        try:
            return ExpertSerializer(obj.expert).data
        except Expert.DoesNotExist:
            pass