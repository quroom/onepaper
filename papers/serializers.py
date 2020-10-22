from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from profiles.serializers import ProfileSerializer
from profiles.models import Profile, ExpertProfile, AuthedUser
from papers.models import Paper, Contractor, Signature

class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ("profile", "profile_id", "paper", "group")

class SignatureSerializer(serializers.ModelSerializer):
    contractor = ContractorSerializer(read_only=True)
    class Meta:
        model = Signature
        fields = "__all__"

class ContractorDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    signature = SignatureSerializer(read_only=True)
    class Meta:
        model = Contractor
        fields = "__all__"

class PaperSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    status_type = serializers.IntegerField(read_only=True)
    paper_contractors = ContractorSerializer(many=True)

    class Meta:
        model = Paper
        fields = '__all__'

    def create(self, validated_data):
        contractors = validated_data.pop('paper_contractors')
        paper = Paper.objects.create(**validated_data)
        for contractor in contractors:
            Contractor.objects.create(profile=contractor['profile'], paper=paper, group=contractor['group'])
        return paper

    def validate(self, data):
        author = self.context['request'].user
        is_author_expert = ExpertProfile.objects.filter(profile__user=author).exists()
        exist_expert = False
        contractors = data['paper_contractors']
        contractors_id_list = []

        for contractor in contractors:
            if contractor['group'] == Contractor.SELLER:
                key = "seller"
            elif contractor['group'] == Contractor.BUYER:
                key = "buyer"
            elif contractor['group'] == Contractor.EXPERT:
                key = "expert"
            
            contractors_id_list.append(contractor['profile'].id)

            if not AuthedUser.objects.filter(authed_users=author, profile=contractor['profile']).exists():
                raise serializers.ValidationError({
                    key: _("프로필 사용 동의 목록에 작성자를 추가하지 않은 프로필은 사용할 수 없습니다."),
                })

            if contractor['group'] == Contractor.SELLER or contractor['group'] == Contractor.BUYER:
                if ExpertProfile.objects.filter(profile=contractor['profile']).exists():
                    raise serializers.ValidationError({
                        key: _("공인중개사는 거래자로 등록할 수 없습니다."),
                    })
            if contractor['group'] == Contractor.EXPERT:
                if ExpertProfile.objects.filter(profile=contractor['profile'], status=ExpertProfile.APPROVED).exists():
                    if not author == contractor['profile'].user:
                        raise serializers.ValidationError({
                            key: _("본인의 프로필을 입력해주세요."),
                        })
                    else:
                        exist_expert = True
                else:
                    raise serializers.ValidationError({
                        key: _("공인중개사로 승인되지 않은 사용자는 계약서에 등록할 수 없습니다."),
                    })

        if contractors_id_list.count(contractor['profile']) > 1:
            #Need to be updated
            #거래자 여러명 되면, key + id로 수정해줘야함.
                raise serializers.ValidationError({
                key: _("같은 사용자를 중복해서 등록할 수 없습니다."),
                })

        if (is_author_expert==True and exist_expert == False):
            raise serializers.ValidationError({
                "expert": _("작성자가 공인중개사인 경우 비워둘 수 없습니다."),
            })
        return data

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, instance):
        return instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")

class PaperReadonlySerializer(PaperSerializer):
    paper_contractors = ContractorDetailSerializer(many=True)
