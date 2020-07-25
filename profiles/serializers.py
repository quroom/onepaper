from django.http import JsonResponse
from rest_framework import serializers
from profiles.models import CustomUser, Profile

class CustomUserSerializer(serializers.ModelSerializer):
    ip_address = serializers.IPAddressField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'ip_address', 'average_response_time',
                  'response_rate', 'contract_success_rate', 'bio', 'used_count',]
        read_only_fields = ('username', 'ip_address', 'average_response_time',
                  'response_rate', 'contract_success_rate', 'bio', 'used_count')

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # signature = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('used_count',)

    def get_user(self, obj):
        return CustomUserSerializer(obj.user).data

class ProfileUnauthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_name']