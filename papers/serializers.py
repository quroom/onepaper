from rest_framework import serializers
from profiles.serializers import ProfileSerializer, ProfileUnauthorizationSerializer
from papers.models import Paper

class PaperSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    expert_profile = serializers.SerializerMethodField()
    seller_profile = serializers.SerializerMethodField()    
    buyer_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = Paper
        fields = '__all__'
        read_only_fields = ('status', 'expert_signature', 'seller_signature', 'buyer_signature')

    def get_expert_profile(self, obj):
        expert_auth_users = getattr(obj.expert, 'authorization_users', None)
        if expert_auth_users is None:
            return None
        else:
            if obj.author in expert_auth_users.all():
                return ProfileSerializer(obj.expert).data
            else:
                return ProfileUnauthorizationSerializer(obj.expert).data

    def get_buyer_profile(self, obj):        
        buyer_auth_users = getattr(obj.buyer, 'authorization_users', None)
        if buyer_auth_users is None:
            return None
        else:
            if obj.author in buyer_auth_users.all():
                return ProfileSerializer(obj.buyer).data
            else:
                return ProfileUnauthorizationSerializer(obj.buyer).data

    def get_seller_profile(self, obj):
        seller_auth_users = getattr(obj.seller, 'authorization_users', None)
        if seller_auth_users is None:
            return None
        else:
            if obj.author in seller_auth_users.all():
                return ProfileSerializer(obj.seller).data
            else:
                return ProfileUnauthorizationSerializer(obj.seller).data