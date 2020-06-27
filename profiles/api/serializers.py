from rest_framework import serializers
from profiles.models import Profile
import re

class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    ip_address = serializers.IPAddressField(read_only=True)
    average_response_time = serializers.FloatField(read_only=True)
    response_rate = serializers.FloatField(read_only=True)
    contract_success_rate = serializers.FloatField(read_only=True)
    average_response_time = serializers.FloatField(read_only=True)
    # signature = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"