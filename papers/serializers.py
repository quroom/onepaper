from rest_framework import serializers
from profiles.serializers import ExpertSerializer, ProfileSerializer
from papers.models import Paper

class PaperSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    expert_profile = serializers.SerializerMethodField()
    seller_profile = serializers.SerializerMethodField()    
    buyer_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = Paper
        fields = '__all__'

    def get_expert_profile(self, obj):
        if obj.expert != None:
            return ExpertSerializer(obj.expert.profile.expert).data
        else:
            return None

    def get_buyer_profile(self, obj):
        if obj.buyer != None:
            return ProfileSerializer(obj.buyer.profile).data
        else:
            return None

    def get_seller_profile(self, obj):
        if obj.seller != None:
            return ProfileSerializer(obj.seller.profile).data
        else:
            return None