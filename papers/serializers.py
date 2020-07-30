from rest_framework import serializers
from profiles.serializers import GeneralProfileSerializer, ProfileNameSerializer
from profiles.models import Profile, Expert
from papers.models import Paper, Signature

class PaperSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
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
        self.fields['seller'].queryset = authorization_user_profiles
        self.fields['buyer'].queryset = authorization_user_profiles

    def get_expert_profile(self, obj):
        expert_auth_users = getattr(obj.expert, 'authorization_users', None)
        if expert_auth_users is None:
            return None
        else:
            if obj.author in expert_auth_users.all():
                return GeneralProfileSerializer(obj.expert).data
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