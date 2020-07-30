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
        self.fields['expert'].queryset = Expert.objects.filter(profile__authorization_users=user)
        authorization_users = Profile.objects.filter(authorization_users=user)
        self.fields['seller'].queryset = authorization_users
        self.fields['buyer'].queryset = authorization_users

    def get_expert_profile(self, obj):
        profile = getattr(obj.expert, 'profile', None)
        if profile is None:
            return None
        else:
            expert_auth_users = getattr(profile, 'authorization_users', None)
            if expert_auth_users is None:
                return None
            else:
                if obj.author in expert_auth_users.all():
                    return GeneralProfileSerializer(obj.expert.profile).data
                else:
                    return ProfileNameSerializer(obj.expert.profile).data

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