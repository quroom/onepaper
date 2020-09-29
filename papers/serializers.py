from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from profiles.serializers import ExpertProfileSerializer, GeneralProfileSerializer, ProfileNameSerializer
from profiles.models import Profile, Expert
from papers.models import Paper, Contractor, Signature

#Later: AddPaperListSerializer, Because Paperserializer is too much heavy.

class PaperSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    status_type = serializers.IntegerField(read_only=True)
    expert_profile = serializers.SerializerMethodField()
    seller_profile = serializers.SerializerMethodField()    
    buyer_profile = serializers.SerializerMethodField()
    expert_signature = serializers.SerializerMethodField()
    seller_signature = serializers.SerializerMethodField()
    buyer_signature = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        fields = '__all__'

    def validate(self, data):
        author = self.context['request'].user
        is_author_expert = Expert.objects.filter(user = author).exists()
        expert_profile = data['expert']
        seller_profile = data['seller']
        buyer_profile = data['buyer']
        expert = getattr(data['expert'], 'user', None)
        seller = data['seller'].user
        buyer = data['buyer'].user

        if (is_author_expert==True and expert_profile == None):
            raise serializers.ValidationError({
                "expert": _("작성자가 공인중개사인 경우 비워둘 수 없습니다."),
            })
        if Expert.objects.filter(user=seller).exists():
            raise serializers.ValidationError({
                "seller": _("공인중개사는 거래자로 등록할 수 없습니다."),
            })
        if Expert.objects.filter(user=buyer).exists():
            raise serializers.ValidationError({
                "buyer": _("공인중개사는 거래자로 등록할 수 없습니다."),
            })
        if not author in seller_profile.authorization_users.all():
            raise serializers.ValidationError({
                "seller": _("프로필 사용 동의를 하지 않은 프로필은 추가할 수 없습니다."),
            })
        if not author in buyer_profile.authorization_users.all():
            raise serializers.ValidationError({
                "buyer": _("프로필 사용 동의를 하지 않은 프로필은 추가할 수 없습니다."),
            })
        if seller == buyer:
            raise serializers.ValidationError({
                "buyer": _("매도(임대)인과 매수(임차)인은 동일할 수 없습니다."),
                "seller": _("매도(임대)인과 매수(임차)인은 동일할 수 없습니다.")
            })
 
        if expert != None:
            if not expert_profile in author.profiles.all():
                raise serializers.ValidationError({
                "expert": _("본인의 프로필을 입력해주세요."),
                })
            if Expert.objects.filter(user=expert).exists() == False:
                raise serializers.ValidationError({
                "expert": _("공인중개사로 인증되지 않은 사용자는 등록할 수 없습니다."),
                })        
        if expert == seller:
            raise serializers.ValidationError({
                "expert": _("공인중개사와 매도(임대)인은 동일할 수 없습니다."),
                "seller": _("공인중개사와 매도(임대)인은 동일할 수 없습니다.")
            })
        if expert == buyer:
            raise serializers.ValidationError({
                "expert": _("공인중개사와 매수(임차)인은 동일할 수 없습니다."),
                "seller": _("공인중개사와 매수(임차)인은 동일할 수 없습니다.")
            })        
        return data

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, instance):
        return instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_expert_profile(self, obj):
        expert = Contractor.objects.filter(paper=obj, group=Contractor.EXPERT).first()
        if expert is None:
            return None
        else:
            return ExpertProfileSerializer(obj.expert).data

    def get_buyer_profile(self, obj):
        buyer = Contractor.objects.filter(paper=obj, group=Contractor.BUYER).first()
        if buyer is None:
            return None
        else:
            return GeneralProfileSerializer(obj.buyer).data

    def get_seller_profile(self, obj):
        seller = Contractor.objects.filter(paper=obj, group=Contractor.SELLER).first()
        if seller is None:
            return None
        else:
            return GeneralProfileSerializer(obj.seller).data

    def get_expert_signature(self, obj):
        expert = getattr(obj.expert, 'user', None)
        if(expert is None):
            return None
        
        signatures = obj.paper_signatures.filter(user=expert)
        if signatures.exists():
            return SignatureSerializer(signatures.first()).data
        else:
            return None

    def get_seller_signature(self, obj):
        seller = getattr(obj.seller, 'user', None)
        if(seller is None):
            return None

        signatures = obj.paper_signatures.filter(user=seller)
        if signatures.exists():
            return SignatureSerializer(signatures.first()).data
        else:
            return None

    def get_buyer_signature(self, obj):
        buyer = getattr(obj.buyer, 'user', None)
        if(buyer is None):
            return None
        
        signatures = obj.paper_signatures.filter(user=buyer)
        if signatures.exists():
            return SignatureSerializer(signatures.first()).data
        else:
            return None

class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = "__all__"

import base64
from django.core.files.base import ContentFile

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class SignatureSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None, use_url=False,
    )
    class Meta:
        model = Signature
        fields = "__all__"
        read_only_fields = ("paper", "user", "image")
