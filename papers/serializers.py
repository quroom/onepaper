import datetime
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import fields
from rest_framework import serializers
from addresses.models import Address
from addresses.serializers import AddressSerializer
from profiles.models import Profile, ExpertProfile, AllowedUser
from profiles.serializers import ProfileSerializer, ProfileBasicInfoSerializer
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

class VerifyingEveryoneExplanationSerializer(VerifyingExplanationSerializer):
    address = serializers.SerializerMethodField()

    def get_address(self, instance):
        address_with_bun = instance.address.old_address.split("-")[0]
        hidden_address = address_with_bun[0:address_with_bun.rindex(" ")]
        return {"old_address": hidden_address}

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
    is_allowed = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Contractor
        fields = ("id", "profile", "profile_id", "paper", "group", "is_allowed")

class ContractorReadSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    signature = SignatureSerializer(read_only=True)
    explanation_signature = ExplanationSignatureSerializer(read_only=True)

    class Meta:
        model = Contractor
        fields = "__all__"

class ContractorUnalloweUserSerializer(serializers.ModelSerializer):
    profile = ProfileBasicInfoSerializer(read_only=True)

    class Meta:
        model = Contractor
        fields = "__all__"

class PaperListSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    updated_at = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(read_only=True)
    status = serializers.SerializerMethodField()
    paper_contractors = ContractorSerializer(many=True)

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

    @transaction.atomic
    def create(self, validated_data):
        verifying_explanation_data = validated_data.pop('verifying_explanation') if not validated_data.get('verifying_explanation') is None else None
        address_data = validated_data.pop('address')
        contractors_data = validated_data.pop('paper_contractors')
        status_instance = PaperStatus.objects.create(status=PaperStatus.DRAFT)
        address = Address.objects.create(**address_data)

        paper = Paper.objects.create(**validated_data, address=address, status=status_instance)

        for contractor_data in contractors_data:
            status_saved = False
            Contractor.objects.create(profile=contractor_data['profile'], paper=paper, group=contractor_data['group'], is_allowed=contractor_data['is_allowed'])
            if status_saved == False and contractor_data['is_allowed'] == False:
                status_instance.status = PaperStatus.REQUESTING
                status_instance.save()
                status_saved = True

        if self.context['request'].user.is_expert == True:
            verifying_explanation_address_data = verifying_explanation_data.pop('address')
            address = Address.objects.create(**verifying_explanation_address_data)
            VerifyingExplanation.objects.create(paper=paper, address=address, **verifying_explanation_data)
        return paper

    @transaction.atomic
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address') if not validated_data.get('address') is None else {}
        contractors_data = validated_data.pop('paper_contractors') if not validated_data.get('paper_contractors') is None else {}
        verifying_explanation_data = validated_data.pop('verifying_explanation') if not validated_data.get('verifying_explanation') is None else {}
        address = instance.address
        contractors = instance.paper_contractors.all()

        for key, val in address_data.items():
            setattr(address, key, val)
        address.save()

        for contractor_data in contractors_data:
            #Ignore is_allowed. Because after instance created, is_allowed value might be changed by each user.
            contractor_data.pop("is_allowed")
            matched = False
            status_saved = False
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
                 Contractor.objects.create(profile=contractor_data['profile'], paper=instance, group=contractor_data['group'], is_allowed=contractor_data['is_allowed'])

        if self.context['request'].user.is_expert == True:
            verifying_explanation = instance.verifying_explanation
            verifying_explanation_address = instance.verifying_explanation.address
            verifying_explanation_address_data = verifying_explanation_data.pop('address') if not verifying_explanation_data.get('address') is None else {}
            
            for key in ['dong', 'ho']:
                if not key in verifying_explanation_address_data:
                    setattr(verifying_explanation_address, key, '')
            for key, val in verifying_explanation_address_data.items():
                setattr(verifying_explanation_address, key, val)
            verifying_explanation_address.save()
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
        contractors = data['paper_contractors'] if not data.get('paper_contractors') is None else []
        users_id_list = []
        for index, contractor in enumerate(contractors):
            if contractor['group'] == Contractor.SELLER:
                key = "seller"
            elif contractor['group'] == Contractor.BUYER:
                key = "buyer"
            elif contractor['group'] == Contractor.EXPERT:
                key = "expert"
            
            users_id_list.append(contractor['profile'].user.id)

            if users_id_list.count(contractor['profile'].user.id) > 1:
                #FIXME Need to be updated
                #거래자 여러명 되면, key + id로 수정해줘야함.
                raise serializers.ValidationError({
                    key: _("같은 회원을 중복해서 등록할 수 없습니다."),
                })
            if not AllowedUser.objects.filter(allowed_users=author, profile=contractor['profile']).exists():
                if author != contractor['profile'].user:
                   contractor['is_allowed'] = False
                else:
                    contractor['is_allowed'] = True
            else:
                contractor['is_allowed'] = True
            if contractor['group'] == Contractor.SELLER or contractor['group'] == Contractor.BUYER:
                if ExpertProfile.objects.filter(profile=contractor['profile']).exists():
                    raise serializers.ValidationError({
                        key: _("공인중개사는 거래자로 등록할 수 없습니다."),
                    })
            if contractor['group'] == Contractor.EXPERT:
                if ExpertProfile.objects.filter(profile=contractor['profile'], status=ExpertProfile.APPROVED).exists():
                    exist_expert = True
                else:
                    raise serializers.ValidationError({
                        key: _("공인중개사로 승인되지 않은 사용자는 계약서에 등록할 수 없습니다."),
                    })
        if self.context['request'].method in ["PUT", "POST"]:
            if author.is_expert==True:
                if exist_expert == False:
                    raise serializers.ValidationError({
                        "expert": _("작성자가 공인중개사인 경우 비워둘 수 없습니다."),
                    })
                if data.get("verifying_explanation") is None:
                    raise serializers.ValidationError({
                        "verifying_explanation": _("작성자가 공인중개사인 경우 확인설명서를 비워둘 수 없습니다."),
                    })
            if not author.id in users_id_list:
                raise serializers.ValidationError({
                    "seller": _("작성자가 포함되지 않았습니다."),
                    "buyer": _("작성자가 포함되지 않았습니다.")
                })
        return data

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

    def get_status(self, instance):
        return instance.status.status

class PaperLoadSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer(read_only=True)
    options = fields.MultipleChoiceField(choices=Paper.OPTIONS_CATEGORY)
    updated_at = serializers.SerializerMethodField()
    verifying_explanation = VerifyingExplanationSerializer(required=False, read_only=True)

    class Meta:
        model = Paper
        fields = "__all__"

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

class PaperReadonlySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer(read_only=True)
    paper_contractors = ContractorReadSerializer(many=True)
    options = fields.MultipleChoiceField(choices=Paper.OPTIONS_CATEGORY)
    status = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    verifying_explanation = VerifyingExplanationSerializer(required=False, read_only=True)

    class Meta:
        model = Paper
        fields = "__all__"
        read_only_fields = ("__all__",)

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

    def get_status(self, instance):
        return instance.status.status

class PaperUnalloweUserSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer(read_only=True)
    paper_contractors = ContractorUnalloweUserSerializer(many=True)
    options = fields.MultipleChoiceField(choices=Paper.OPTIONS_CATEGORY)
    status = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    verifying_explanation = VerifyingExplanationSerializer(required=False, read_only=True)

    class Meta:
        model = Paper
        fields = "__all__"
        read_only_fields = ("__all__",)

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

    def get_status(self, instance):
        return instance.status.status

class PaperEveryoneSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    address = serializers.SerializerMethodField()
    options = fields.MultipleChoiceField(choices=Paper.OPTIONS_CATEGORY)
    updated_at = serializers.SerializerMethodField()
    verifying_explanation = VerifyingEveryoneExplanationSerializer(required=False, read_only=True)

    class Meta:
        model = Paper
        fields = "__all__"
        read_only_fields = ("__all__",)

    def get_address(self, instance):
        address_with_bun = instance.address.old_address.split("-")[0]
        hidden_address = address_with_bun[0:address_with_bun.rindex(" ")]
        return {"old_address": hidden_address}

    def get_updated_at(self, instance):
        return (instance.updated_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")