import phonenumbers
from phonenumber_field.serializerfields import PhoneNumberField
from django.http import JsonResponse
from rest_framework import serializers
from profiles.models import CustomUser, Expert, Profile
from papers.models import Paper
from django.db.models import Q

class CustomUserSerializer(serializers.ModelSerializer):
    ip_address = serializers.IPAddressField(read_only=True)
    is_expert = serializers.SerializerMethodField()

    def get_is_expert(self, obj):
        expert = getattr(obj, 'expert', None)
        if expert is None:
            return False
        else:
            return True

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'ip_address', 'is_expert', 'average_response_time',
                  'response_rate', 'contract_success_rate', 'name', 'birthday', 'bio', 'used_count']
        read_only_fields = ('id', 'username', 'ip_address', 'is_expert', 'average_response_time',
                  'response_rate', 'contract_success_rate', 'used_count')

class BaseProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_user(self, obj):
        return CustomUserSerializer(obj.user).data

class ExpertProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = Profile
        exclude = ['address']
        read_only_fields = ('used_count',)

class GeneralProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = Profile
        exclude = ['shop_name', 'shop_address', 'registration_number']
        read_only_fields = ('used_count', 'is_expert')

class ProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'profile_name']

class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = '__all__'