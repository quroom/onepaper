import phonenumbers
from phonenumber_field.serializerfields import PhoneNumberField
from django.http import JsonResponse
from rest_framework import serializers
from profiles.models import CustomUser, Profile, ExpertProfile, AuthedUser
from papers.models import Paper
from django.db.models import Q

class CustomUserSerializer(serializers.ModelSerializer):
    ip_address = serializers.IPAddressField(read_only=True)
    is_expert = serializers.SerializerMethodField()

    def get_is_expert(self, obj):        
        return ExpertProfile.objects.filter(profile__user=obj, status=ExpertProfile.APPROVED).exists()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'ip_address', 'is_expert', 'average_response_time',
                  'response_rate', 'contract_success_rate', 'name', 'birthday', 'bio', 'used_count', 'request_expert']
        read_only_fields = ('id', 'username', 'ip_address', 'is_expert', 'average_response_time',
                  'response_rate', 'contract_success_rate', 'used_count')

class CustomUserIDNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']

class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertProfile
        fields = "__all__"
        read_only_fields = ('profile', 'status',)

class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    expert_profile = ExpertSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ('used_count', 'is_expert')

class ExpertProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    expert_profile = ExpertSerializer()

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ('used_count', 'is_expert')

    def create(self, validated_data):
        expert_profile = validated_data.pop('expert_profile')
        profile = Profile.objects.create(**validated_data)
        ExpertProfile.objects.create(profile=profile, **expert_profile)
        return profile
    
    def update(self, validated_data):
        expert_profile = validated_data.pop('expert_profile')
        profile = Profile.objects.save(**validated_data)
        ExpertProfile.objects.save(profile=profile, **expert_profile)
        return profile

class AuthedUserSerializer(serializers.ModelSerializer):
    authed_users = CustomUserIDNameSerializer(many=True)
    profile = ProfileSerializer()
    class Meta:
        model = AuthedUser
        fields = "__all__"
        read_only_fields = ('profile',)

class AllowedProfileListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = AuthedUser
        fields = ["profile"]
        read_only_fields = ('profile',)
