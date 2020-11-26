from django.utils.translation import ugettext_lazy as _
import phonenumbers
from phonenumber_field.serializerfields import PhoneNumberField
from django.http import JsonResponse
from rest_framework import serializers
from profiles.models import CustomUser, Profile, ExpertProfile, AllowedUser, Mandate
from addresses.models import Address
from addresses.serializers import AddressSerializer
from papers.models import Paper

class CustomUserSerializer(serializers.ModelSerializer):
    ip_address = serializers.IPAddressField(read_only=True)
    is_expert = serializers.SerializerMethodField()
    has_profile = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'ip_address', 'is_expert', 'is_staff', 'has_profile', 'average_response_time',
                  'response_rate', 'contract_success_rate', 'name', 'birthday', 'bio', 'used_count', 'request_expert']
        read_only_fields = ('id', 'username', 'ip_address', 'is_expert', 'is_staff', 'has_profile', 'average_response_time',
                  'response_rate', 'contract_success_rate', 'used_count')

    def get_is_expert(self, obj):
        return ExpertProfile.objects.filter(profile__user=obj, status=ExpertProfile.APPROVED).exists() or obj.request_expert

    def get_has_profile(self, obj):
        return obj.profiles.exists()


class CustomUserIDNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', "name"]

class ApproveExpertSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    birthday = serializers.SerializerMethodField()

    class Meta:
        model = ExpertProfile
        fields = "__all__"
        read_only_fields = ('profile', 'registration_number', 'shop_name', 'registration_certificate', 'agency_license', 'stamp', 'garantee_insurance')

    def get_username(self, obj):
        return obj.profile.user.username
    
    def get_name(self, obj):
        return obj.profile.user.name

    def get_birthday(self, obj):
        return obj.profile.user.birthday

    def get_updated_at(self, instance):
        return instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")

class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertProfile
        fields = "__all__"
        read_only_fields = ('profile', 'status',)

class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    address = AddressSerializer()
    expert_profile = ExpertSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ('used_count', 'is_expert')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)

        profile = Profile.objects.create(**validated_data, address=address)
        return profile
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')

        address = instance.address
        for key in ['dong', 'ho']:
            if not key in address_data:
                setattr(address, key, '')
        for key, val in address_data.items():
            setattr(address, key, val)
        address.save()

        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        return instance

class ExpertProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    expert_profile = ExpertSerializer()
    address = AddressSerializer()

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ('used_count', 'is_expert')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        expert_profile = validated_data.pop('expert_profile')
        address = Address.objects.create(**address_data)

        profile = Profile.objects.create(**validated_data, address=address)
        ExpertProfile.objects.create(profile=profile, **expert_profile)
        return profile
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        expert_profile_data = validated_data.pop('expert_profile')

        address = instance.address
        for key in ['dong', 'ho']:
            if not key in address_data:
                setattr(address, key, '')
        for key, val in address_data.items():
            setattr(address, key, val)
        address.save()
        
        expert_profile = instance.expert_profile
        for key, val in expert_profile_data.items():
            setattr(expert_profile, key, val)
        expert_profile.save()

        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        return instance

class AllowedUserSerializer(serializers.ModelSerializer):
    allowed_users = CustomUserIDNameSerializer(many=True)
    # profile = ProfileSerializer()
    class Meta:
        model = AllowedUser
        fields = "__all__"
        read_only_fields = ('profile',)

class AllowedProfileListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = AllowedUser
        fields = ["profile"]
        read_only_fields = ('profile',)

class MandateReadOnlySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    designator = ProfileSerializer(read_only=True)
    designee = ProfileSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    class Meta:
        model = Mandate
        fields = "__all__"

class MandateSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer()
    class Meta:
        model = Mandate
        fields = "__all__"
    
    def validate(self, data):
        try:
            if data['designator'].user != self.context['request'].user and "designator_signature" in data:
                raise serializers.ValidationError({"signature-button":_("위임인만 서명이 가능합니다.")})
            if data['designator'].user == data['designee'].user:
                raise serializers.ValidationError({"designee":_("위임인과 수임인이 동일할 수 없습니다.")})
        except Profile.DoesNotExist:
            raise serializers.ValidationError(_("사용자가 존재하지 않습니다."))
        return data
    
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        designator = validated_data['designator']
        designee = validated_data['designee']
        allowedUser = AllowedUser.objects.get(profile=designator)
        if not designee in allowedUser.allowed_users.all():
            allowedUser.allowed_users.add(designee.user)
            allowedUser.save()

        address = Address.objects.create(**address_data)

        mandate = Mandate.objects.create(**validated_data, address=address)
        return mandate
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')

        address = instance.address
        for key, val in address_data.items():
            setattr(address, key, val)
        address.save()
        
        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        return instance
