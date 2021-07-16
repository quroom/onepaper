from django.db import transaction
from django.utils.translation import ugettext as _
from rest_framework import fields
from rest_framework import serializers
from addresses.models import Address
from addresses.serializers import AddressSerializer
from profiles.models import ExpertProfile, AllowedUser
from profiles.serializers import InsuranceSerializer, ProfileReadonlySerializer, ProfileBasicInfoSerializer
from papers.models import Paper, Contractor, Signature, PaperStatus, VerifyingExplanation, ExplanationSignature
from onepaper.serializers import ReadOnlyModelSerializer

class ExplanationSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExplanationSignature
        fields = "__all__"

class VerifyingExplanationSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    paper_categories = fields.MultipleChoiceField(choices=VerifyingExplanation.PAPER_CATEGORY)
    explanation_evidences = fields.MultipleChoiceField(choices=VerifyingExplanation.EXPLANATION_EVIDENCE_CATEGORY)

    class Meta:
        model = VerifyingExplanation
        fields = "__all__"
        read_only_fields = ('paper',)

class VerifyingExplanationReadonlySerializer(ReadOnlyModelSerializer):
    address = AddressSerializer()
    paper_categories = fields.MultipleChoiceField(choices=VerifyingExplanation.PAPER_CATEGORY)
    explanation_evidences = fields.MultipleChoiceField(choices=VerifyingExplanation.EXPLANATION_EVIDENCE_CATEGORY)
    insurance = InsuranceSerializer()

    class Meta:
        model = VerifyingExplanation
        fields = "__all__"

class VerifyingEveryoneExplanationSerializer(VerifyingExplanationSerializer):
    address = serializers.SerializerMethodField()

    def get_address(self, instance):
        address_with_bun = instance.address.old_address.split("-")[0]
        hidden_address = address_with_bun[0:address_with_bun.rindex(" ")]
        old_address_eng = instance.address.old_address_eng
        hidden_address_eng = old_address_eng[old_address_eng.index(" ")+1:len(old_address_eng)]
        return {"old_address": hidden_address, "old_address_eng": hidden_address_eng}

class SignatureSerializer(serializers.ModelSerializer):
    paper_status = serializers.SerializerMethodField()

    class Meta:
        model = Signature
        fields = "__all__"


    def get_paper_status(self, instance):
        return instance.contractor.paper.status.status

class ContractorSerializer(serializers.ModelSerializer):
    is_allowed = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Contractor
        fields = ("id", "profile", "profile_id", "paper", "group", "is_allowed")

class ContractorReadonlySerializer(serializers.ModelSerializer):
    profile = ProfileReadonlySerializer(read_only=True)
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

class PaperListSerializer(ReadOnlyModelSerializer):
    address = AddressSerializer()
    author = serializers.StringRelatedField(read_only=True)
    status = serializers.SerializerMethodField()
    answer_count = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        exclude = ["special_agreement"]

    def get_status(self, instance):
        return instance.status.status

    def get_answer_count(self, instance):
        return instance.paper_contractors.get(profile__user=self.context['request'].user).contractor_answers.count()

class PaperSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer()
    likes_count = serializers.SerializerMethodField()
    options = fields.MultipleChoiceField(choices=Paper.OPTIONS_CATEGORY)
    paper_contractors = ContractorSerializer(many=True)
    status = serializers.SerializerMethodField()
    user_has_vote = serializers.SerializerMethodField()
    verifying_explanation = VerifyingExplanationSerializer(required=False)

    class Meta:
        model = Paper
        exclude = ["voters"]

    @transaction.atomic
    def create(self, validated_data):
        verifying_explanation_data = validated_data.pop('verifying_explanation') if not validated_data.get('verifying_explanation') is None else None
        address_data = validated_data.pop('address')
        contractors_data = validated_data.pop('paper_contractors')
        status_instance = PaperStatus.objects.create(status=PaperStatus.DRAFT)
        address = Address.objects.create(**address_data)
        is_paper_requsting = False

        paper = Paper.objects.create(**validated_data, address=address, status=status_instance)

        for contractor_data in contractors_data:
            Contractor.objects.create(profile=contractor_data['profile'], paper=paper, group=contractor_data['group'], is_allowed=contractor_data['is_allowed'])
            if is_paper_requsting == False and contractor_data['is_allowed'] == False:
                status_instance.status = PaperStatus.REQUESTING
                status_instance.save()
                is_paper_requsting = True

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
        status_instance  = instance.status
        address = instance.address
        is_paper_requsting = False
        contractors_profile = []
        for contractor_data in contractors_data:
            contractors_profile.append(contractor_data.get("profile"))
        deleted_contractors = instance.paper_contractors.exclude(profile__in=contractors_profile)
        deleted_contractors.delete()

        for key, val in address_data.items():
            setattr(address, key, val)
        address.save()

        for contractor_data in contractors_data:
            try:
                obj = Contractor.objects.get(profile=contractor_data['profile'], paper=instance)
                setattr(obj, 'group', contractor_data['group'])
                setattr(obj, 'is_allowed', contractor_data['is_allowed'])
                obj.save()
            except Contractor.DoesNotExist:
                try:
                    obj = Contractor.objects.get(paper=instance, group=contractor_data['group'])
                    setattr(obj, 'profile', contractor_data['profile'])
                except Contractor.DoesNotExist:
                    obj = Contractor.objects.create(**contractor_data)
                    obj.save()

            if is_paper_requsting == False and contractor_data['is_allowed'] == False:
                status_instance.status = PaperStatus.REQUESTING
                status_instance.save()
                is_paper_requsting = True

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
        exist_expert = False
        expert_profile = None
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

            if author != contractor['profile'].user:
                if not AllowedUser.objects.filter(allowed_users=author, profile=contractor['profile']).exists():
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
                if ExpertProfile.objects.filter(profile=contractor['profile'], profile__is_default=True, status=ExpertProfile.APPROVED).exists():
                    exist_expert = True
                    if contractor['profile'].user == author:
                        expert_profile = contractor['profile']
                else:
                    raise serializers.ValidationError({
                        key: _("승인 및 활성화되지 않은 공인중개사 프로필은 계약서에 등록할 수 없습니다."),
                    })

        if self.context['request'].method in ["PUT", "POST"]:
            if author.is_expert == True:
                if exist_expert == False:
                    raise serializers.ValidationError({
                        "expert": _("작성자가 공인중개사인 경우 비워둘 수 없습니다."),
                    })
                ve = data.get("verifying_explanation")
                if ve is None:
                    raise serializers.ValidationError({
                        "verifying_explanation": _("작성자가 공인중개사인 경우 확인설명서를 비워둘 수 없습니다."),
                    })
                else:
                    insurance = ve.get('insurance')
                    if not insurance.expert_profile.profile.id == expert_profile.id:
                        raise serializers.ValidationError({
                            "insurance": _("보유하지 않은 중개보증서류가 추가되었습니다."),
                        })
            if not author.id in users_id_list:
                raise serializers.ValidationError({
                    "seller": _("작성자가 포함되지 않았습니다."),
                    "buyer": _("작성자가 포함되지 않았습니다.")
                })
        return data

    def get_status(self, instance):
        return instance.status.status

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_vote(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

class PaperLoadSerializer(ReadOnlyModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer(read_only=True)
    options = fields.MultipleChoiceField(choices=Paper.OPTIONS_CATEGORY)
    verifying_explanation = VerifyingExplanationSerializer(required=False, read_only=True)

    class Meta:
        model = Paper
        fields = "__all__"

class PaperReadonlySerializer(ReadOnlyModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer(read_only=True)
    paper_contractors = ContractorReadonlySerializer(many=True)
    options = fields.MultipleChoiceField(choices=Paper.OPTIONS_CATEGORY)
    status = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    verifying_explanation = VerifyingExplanationReadonlySerializer()
    user_has_vote = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        fields = "__all__"

    def get_status(self, instance):
        return instance.status.status

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_vote(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

class PaperUnalloweUserSerializer(ReadOnlyModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer(read_only=True)
    options = fields.MultipleChoiceField(choices=Paper.OPTIONS_CATEGORY)
    paper_contractors = ContractorUnalloweUserSerializer(many=True)
    status = serializers.SerializerMethodField()
    verifying_explanation = VerifyingExplanationSerializer(required=False, read_only=True)

    class Meta:
        model = Paper
        exclude = ["voters"]

    def get_status(self, instance):
        return instance.status.status

class PaperUnalloweUserDetailSerializer(PaperUnalloweUserSerializer):
    likes_count = serializers.SerializerMethodField()
    user_has_vote = serializers.SerializerMethodField()

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_vote(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

class PaperEveryoneSerializer(ReadOnlyModelSerializer):
    author = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    is_contractor = serializers.SerializerMethodField()
    options = fields.MultipleChoiceField(choices=Paper.OPTIONS_CATEGORY)
    status = serializers.SerializerMethodField()
    verifying_explanation = VerifyingEveryoneExplanationSerializer(required=False, read_only=True)

    class Meta:
        model = Paper
        exclude = ["voters"]

    def get_author(self, instance):
        if instance.is_contractor:
            return str(instance.author)
        else:
            return ''

    def get_address(self, instance):
        if instance.is_contractor:
            return {"old_address": instance.address.old_address, "old_address_eng": instance.address.old_address_eng}
        address_with_bun = instance.address.old_address.split("-")[0]
        hidden_address = address_with_bun[0:address_with_bun.rindex(" ")]
        old_address_eng = instance.address.old_address_eng
        hidden_address_eng = old_address_eng[old_address_eng.index(" ")+1:len(old_address_eng)]
        return {"old_address": hidden_address, "old_address_eng": hidden_address_eng}

    def get_is_contractor(self, instance):
        return instance.is_contractor

    def get_status(self, instance):
        return instance.status.status

class PaperEveryoneDetailSerializer(PaperEveryoneSerializer):
    likes_count = serializers.SerializerMethodField()
    user_has_vote = serializers.SerializerMethodField()
    is_contractor = None
    author = None

    class Meta:
        model = Paper
        exclude = ["voters", "author",]

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_vote(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

    def get_author(self, instance):
        return ''

    def get_address(self, instance):
        address_with_bun = instance.address.old_address.split("-")[0]
        hidden_address = address_with_bun[0:address_with_bun.rindex(" ")]
        old_address_eng = instance.address.old_address_eng
        hidden_address_eng = old_address_eng[old_address_eng.index(" ")+1:len(old_address_eng)]
        return {"old_address": hidden_address, "old_address_eng": hidden_address_eng}