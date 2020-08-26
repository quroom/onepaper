from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from profiles.serializers import ExpertProfileSerializer, GeneralProfileSerializer, ProfileNameSerializer
from profiles.models import Profile, Expert
from papers.models import Paper, Signature

#Later: AddPaperListSerializer, Because Paperserializer is too much heavy.

class PaperSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    status_type = serializers.IntegerField(read_only=True)
    expert_profile = serializers.SerializerMethodField()
    seller_profile = serializers.SerializerMethodField()    
    buyer_profile = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user

        super(PaperSerializer, self).__init__(*args, **kwargs)
        authorization_user_profiles = Profile.objects.filter(authorization_users=user)
        self.fields['expert'].queryset = authorization_user_profiles.filter(expert__isnull=False)
        self.fields['seller'].queryset = authorization_user_profiles.filter(expert__isnull=True)
        self.fields['buyer'].queryset = authorization_user_profiles.filter(expert__isnull=True)

    def validate(self, data):
        if getattr(data['expert'], 'user', None) == data['seller'].user:
            raise serializers.ValidationError({
                "expert": _("전문가와 매도(임대)인은 동일할 수 없습니다."),
                "seller": _("전문가와 매도(임대)인은 동일할 수 없습니다.")
            })
        if getattr(data['expert'], 'user', None) == data['buyer'].user:
            raise serializers.ValidationError({
                "expert": _("전문가와 매수(임차)인은 동일할 수 없습니다."),
                "seller": _("전문가와 매수(임차)인은 동일할 수 없습니다.")
            })
        if data['seller'].user == data['buyer'].user:
            raise serializers.ValidationError({
                "buyer": _("매도(임대)인과 매수(임차)인은 동일할 수 없습니다."),
                "seller": _("매도(임대)인과 매수(임차)인은 동일할 수 없습니다.")
            })
        return data

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, instance):
        return instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_expert_profile(self, obj):
        expert_auth_users = getattr(obj.expert, 'authorization_users', None)
        if expert_auth_users is None:
            return None
        else:
            if obj.author in expert_auth_users.all():
                return ExpertProfileSerializer(obj.expert).data
            else:
                return ProfileNameSerializer(obj.expert).data

    def get_buyer_profile(self, obj):        
        buyer_auth_users = getattr(obj.buyer, 'authorization_users', None)
        if buyer_auth_users is None:
            return None
        else:
            if obj.author in buyer_auth_users.all():
                return GeneralProfileSerializer(obj.buyer).data
            else:
                return ProfileNameSerializer(obj.buyer).data

    def get_seller_profile(self, obj):
        seller_auth_users = getattr(obj.seller, 'authorization_users', None)
        if seller_auth_users is None:
            return None
        else:
            if obj.author in seller_auth_users.all():
                return GeneralProfileSerializer(obj.seller).data
            else:
                return ProfileNameSerializer(obj.seller).data

class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        fields = "__all__"
        read_only_fields = ("paper", "profile")