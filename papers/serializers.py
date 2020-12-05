import datetime
from django.utils.translation import ugettext_lazy as _
from rest_framework import fields
from rest_framework import serializers
from addresses.models import Address
from addresses.serializers import AddressSerializer
from profiles.models import Profile, ExpertProfile, AllowedUser
from profiles.serializers import ProfileSerializer
from papers.models import Paper, Contractor, Signature, PaperStatus, VerifyingExplanation, ExplanationSignature

class ExplanationSignatureSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = ExplanationSignature
        fields = "__all__"

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

class VerifyingExplanationSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    paper_categories = fields.MultipleChoiceField(choices=VerifyingExplanation.PAPER_CATEGORY)
    explanation_evidences = fields.MultipleChoiceField(choices=VerifyingExplanation.EXPLANATION_EVIDENCE_CATEGORY)
    
    class Meta:
        model = VerifyingExplanation
        fields = "__all__"
        read_only_fields = ('paper',)

class SignatureSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()
    paper_status = serializers.SerializerMethodField()

    class Meta:
        model = Signature
        fields = "__all__"

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

    def get_paper_status(self, instance):
        return instance.contractor.paper.status.status

class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ("id", "profile", "profile_id", "paper", "group")

class ContractorReadSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    signature = SignatureSerializer(read_only=True)
    explanation_signature = ExplanationSignatureSerializer(read_only=True)
    
    class Meta:
        model = Contractor
        fields = "__all__"

class PaperListSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    updated_at = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(read_only=True)
    paper_contractors = ContractorReadSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        exclude = ["special_agreement"]
        read_only_fields = ("__all__",)

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

    def get_status(self, instance):
        return instance.status.status

class PaperSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    updated_at = serializers.SerializerMethodField()
    address = AddressSerializer()
    options = fields.MultipleChoiceField(choices=Paper.OPTIONS_CATEGORY)
    paper_contractors = ContractorSerializer(many=True)
    verifying_explanation = VerifyingExplanationSerializer(required=False)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        fields = "__all__"

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        contractors_data = validated_data.pop('paper_contractors')
        verifying_explanation_data = validated_data.pop('verifying_explanation') if not validated_data.get('verifying_explanation') is None else None
        status = PaperStatus.objects.create(status=PaperStatus.DRAFT)
        address = Address.objects.create(**address_data)

        paper = Paper.objects.create(**validated_data, address=address, status=status)

        for contractor_data in contractors_data:
            Contractor.objects.create(profile=contractor_data['profile'], paper=paper, group=contractor_data['group'])
        
        if not verifying_explanation_data is None:
            verifying_explanation_address_data = verifying_explanation_data.pop('address')
            address = Address.objects.create(**verifying_explanation_address_data)
            VerifyingExplanation.objects.create(paper=paper, address=address, **verifying_explanation_data)
        return paper
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        contractors_data = validated_data.pop('paper_contractors')
        verifying_explanation_data = validated_data.pop('verifying_explanation') if not validated_data.get('verifying_explanation') is None else None
        address = instance.address
        contractors = instance.paper_contractors.all()

        for key in ['dong', 'ho']:
            if not key in address_data:
                setattr(address, key, '')
        for key, val in address_data.items():
            setattr(address, key, val)
        address.save()

        for contractor_data in contractors_data:
            matched = False
            for contractor in contractors:
                if contractor_data['paper'] == None:
                    matched = True
                    contractors.get(group=contractor_data['group']).delete()
                    break
                if contractor_data['group'] == contractor.group:
                    matched = True
                    for key, val in contractor_data.items():
                        if not val is None:
                            setattr(contractor, key, val)
                    contractor.save()
            if matched == False:
                 Contractor.objects.create(profile=contractor_data['profile'], paper=instance, group=contractor_data['group'])

        if not verifying_explanation_data is None:
            verifying_explanation = instance.verifying_explanation
            verifying_explanation_addres = instance.verifying_explanation.address
            verifying_explanation_address_data = verifying_explanation_data.pop('address')
            
            for key in ['dong', 'ho']:
                if not key in verifying_explanation_address_data:
                    setattr(verifying_explanation_addres, key, '')
            for key, val in verifying_explanation_address_data.items():
                setattr(verifying_explanation_addres, key, val)
            verifying_explanation_addres.save()
            for key, val in verifying_explanation_data.items():
                setattr(verifying_explanation, key, val)
            verifying_explanation.save()

        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()

        return instance

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

            if not AllowedUser.objects.filter(allowed_users=author, profile=contractor['profile']).exists():
                if author != contractor['profile'].user:
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

            if contractors_id_list.count(contractor['profile'].id) > 1:
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

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

    def get_status(self, instance):
        return instance.status.status

class PaperReadonlySerializer(PaperSerializer):
    address = AddressSerializer()
    verifying_explanation = VerifyingExplanationSerializer()
    paper_contractors = ContractorReadSerializer(many=True)
    status = serializers.SerializerMethodField()
    
    def get_status(self, instance):
        return instance.status.status
