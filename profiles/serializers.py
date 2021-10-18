import datetime

import phonenumbers
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import ugettext as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from addresses.models import Address
from addresses.serializers import AddressSerializer
from onepaper.serializers import ReadOnlyModelSerializer
from papers.models import Contractor, Paper
from profiles.models import (
    AllowedUser,
    Certification,
    CustomUser,
    ExpertProfile,
    Insurance,
    Mandate,
    Profile,
    UserSetting,
)


class CustomUserIDNameSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["name", "email", "is_expert"]


class ApproveExpertSerializer(ReadOnlyModelSerializer):
    birthday = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(source="profile.updated_at")
    insurance = serializers.SerializerMethodField()

    class Meta:
        model = ExpertProfile
        fields = "__all__"

    def get_birthday(self, obj):
        return obj.profile.user.birthday

    def get_email(self, obj):
        return obj.profile.user.email

    def get_name(self, obj):
        return obj.profile.user.name

    def get_insurance(self, obj):
        date = timezone.localtime().strftime("%Y-%m-%d")
        try:
            return InsuranceSerializer(
                obj.insurances.get(from_date__lte=date, to_date__gte=date)
            ).data
        except Insurance.DoesNotExist:
            return InsuranceSerializer(None).data


class BasicCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "updated_at", "is_expert", "email", "bio", "name", "birthday"]
        read_only_fields = ("id", "updated_at", "is_expert", "email")


class CertificationSerializer(ReadOnlyModelSerializer):
    is_certificated = serializers.SerializerMethodField()

    class Meta:
        model = Certification
        fields = ["id", "updated_at", "is_certificated"]

    def get_is_certificated(self, obj):
        if obj.di != "":
            return True
        else:
            return False


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        exclude = ["user"]


class CustomUserSerializer(serializers.ModelSerializer):
    has_profile = serializers.SerializerMethodField()
    user_setting = UserSettingSerializer()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "updated_at",
            "email",
            "is_expert",
            "is_staff",
            "has_profile",
            "bio",
            "name",
            "birthday",
            "user_setting",
        ]
        read_only_fields = ("id", "updated_at", "email", "is_expert", "is_staff", "has_profile")

    def get_has_profile(self, obj):
        return obj.profiles.exists()


class CustomUserHiddenIDNameSerializer(serializers.ModelSerializer):
    birthday = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["birthday", "email", "name"]

    def get_birthday(self, obj):
        return len(str(obj.birthday)[0:4]) * "#" + str(obj.birthday)[4:]

    def get_email(self, obj):
        if self.context.get("request").user == obj:
            return obj.email
        email_id = obj.email.split("@")[0]
        email_id_len_half = int(len(email_id) / 2)
        return email_id_len_half * "#" + obj.email[email_id_len_half:]

    def get_name(self, obj):
        return obj.name[0:1] + len(obj.name[1:2]) * "#" + obj.name[2:]


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = "__all__"
        read_only_fields = ("expert_profile",)
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }

    def validate(self, data):
        from_date = data.get("from_date")
        profile_pk = self.context.get("profile_pk")
        pk = self.context.get("pk")
        insurnaces = Insurance.objects.filter(
            expert_profile__profile=profile_pk, from_date__lte=from_date, to_date__gte=from_date
        )
        if pk != None:
            insurnaces = insurnaces.exclude(id=pk)
        if insurnaces.exists():
            raise serializers.ValidationError({"dates": _("기존 보증서류와 기간이 중복될 수 없습니다.")})
        return data


class ExpertSerializer(serializers.ModelSerializer):
    insurance = InsuranceSerializer()

    class Meta:
        model = ExpertProfile
        fields = "__all__"
        read_only_fields = (
            "profile",
            "status",
        )


class ExpertReadonlySerializer(ReadOnlyModelSerializer):
    insurance = serializers.SerializerMethodField()
    insurance_count = serializers.SerializerMethodField()

    class Meta:
        model = ExpertProfile
        fields = "__all__"

    def get_insurance(self, obj):
        date = timezone.localtime().strftime("%Y-%m-%d")
        try:
            return InsuranceSerializer(
                obj.insurances.get(from_date__lte=date, to_date__gte=date)
            ).data
        except Insurance.DoesNotExist:
            return InsuranceSerializer(None).data

    def get_insurance_count(self, obj):
        return obj.insurances.count()


class ProfileBasicInfoSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    certification = CertificationSerializer(read_only=True)
    expert_profile = ExpertReadonlySerializer(read_only=True)
    mobile_number = serializers.SerializerMethodField()
    user = CustomUserHiddenIDNameSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["address", "certification", "expert_profile", "id", "mobile_number", "user"]

    def get_address(self, instance):
        address_with_bun = instance.address.old_address.split("-")[0]
        hidden_address = address_with_bun[0 : address_with_bun.rindex(" ")]
        return {"old_address": hidden_address}

    def get_mobile_number(self, obj):
        return obj.mobile_number.raw_input[:-2] + len(obj.mobile_number.raw_input[-2:]) * "#"


class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    certification = CertificationSerializer(read_only=True)
    user = BasicCustomUserSerializer(read_only=True)
    expert_profile = ExpertSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("is_activated",)

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)
        profile = Profile.objects.create(**validated_data, address=address)
        Certification.objects.create(profile=profile)
        allowedUser = AllowedUser.objects.create(profile=profile)
        allowedUser.allowed_users.add(validated_data["user"])
        allowedUser.save()
        return profile

    @transaction.atomic
    def update(self, instance, validated_data):
        address_data = (
            validated_data.pop("address") if not validated_data.get("address") is None else {}
        )
        address = instance.address

        for key in ["dong", "ho"]:
            if not key in address_data:
                setattr(address, key, "")
        for key, val in address_data.items():
            setattr(address, key, val)
        address.save()

        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        return instance


class ProfileReadonlySerializer(ReadOnlyModelSerializer):
    address = AddressSerializer()
    certification = CertificationSerializer(read_only=True)
    expert_profile = ExpertReadonlySerializer()
    user = BasicCustomUserSerializer()

    class Meta:
        model = Profile
        fields = "__all__"


class ExpertProfileReadonlySerializer(ReadOnlyModelSerializer):
    address = AddressSerializer()
    certification = CertificationSerializer(read_only=True)
    expert_profile = ExpertReadonlySerializer()
    user = BasicCustomUserSerializer()

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("is_activated",)


class ExpertProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    expert_profile = ExpertSerializer()
    user = BasicCustomUserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("is_activated",)

    def validate_image(self, image, field_name):
        file_size = image.size
        max_size = 1024 * 1024
        if file_size > max_size:
            raise serializers.ValidationError(
                {field_name: _("Max size of file is %(size)s KB") % {"size": max_size}}
            )

    def validate(self, data):
        for key, value in data["expert_profile"].items():
            if hasattr(data["expert_profile"][key], "file"):
                self.validate_image(value, key)
        return data

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop("address")
        expert_profile = validated_data.pop("expert_profile")
        insurance_data = expert_profile.pop("insurance")

        with transaction.atomic():
            address = Address.objects.create(**address_data)
            profile = Profile.objects.create(**validated_data, address=address)
            Certification.objects.create(profile=profile)
            expert_profile = ExpertProfile.objects.create(profile=profile, **expert_profile)
            Insurance.objects.create(**insurance_data, expert_profile=expert_profile)
            allowedUser = AllowedUser.objects.create(profile=profile)
            allowedUser.allowed_users.add(validated_data["user"])
            allowedUser.save()
        return profile

    @transaction.atomic
    def update(self, instance, validated_data):
        address_data = (
            validated_data.pop("address") if not validated_data.get("address") is None else {}
        )
        expert_profile_data = (
            validated_data.pop("expert_profile")
            if not validated_data.get("expert_profile") is None
            else {}
        )
        insurance_data = (
            expert_profile_data.pop("insurance")
            if not expert_profile_data.get("insurance") is None
            else {}
        )

        address = instance.address
        for key in ["dong", "ho"]:
            if not key in address_data:
                setattr(address, key, "")
        for key, val in address_data.items():
            setattr(address, key, val)
        address.save()

        expert_profile = instance.expert_profile
        for key, val in expert_profile_data.items():
            setattr(expert_profile, key, val)
        expert_profile.save()

        # today = datetime.datetime.now().strftime("%Y-%m-%d")
        insurance_id = insurance_data.get("id")
        if insurance_id:
            insurance = Insurance.objects.get(id=insurance_id)
            for key, value in insurance_data.items():
                setattr(insurance, key, value)
            insurance.save()

        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        return instance


class MandateEveryoneSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    designator = ProfileBasicInfoSerializer(read_only=True)
    designee = ProfileBasicInfoSerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Mandate
        fields = "__all__"


class MandateReadOnlySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    designator = ProfileReadonlySerializer(read_only=True)
    designee = ProfileReadonlySerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Mandate
        fields = "__all__"


class MandateSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer()

    class Meta:
        model = Mandate
        fields = "__all__"

    def validate(self, data):
        try:
            designator = data["designator"]
            designee = data["designee"]
            request_user = self.context["request"].user

            if data.get("address") != None:
                mandates = Mandate.objects.filter(
                    address__old_address=data["address"]["old_address"],
                    designator=designator,
                    designee=designee,
                    to_date__gte=data["from_date"],
                ).exclude(designator_signature="")
                if mandates.exists():
                    mandate_id = mandates.first().id
                    raise serializers.ValidationError(
                        {
                            "period": _("위임 기간이 중복될 수 없습니다.(중복ID:%(mandate_id)s)")
                            % {"mandate_id": mandate_id}
                        }
                    )

            if hasattr(designee, "expert_profile"):
                if designee.expert_profile.status != ExpertProfile.APPROVED:
                    raise serializers.ValidationError(
                        {"designator": _("공인중개사로 승인되지 않은 사용자는 위임장에 등록할 수 없습니다.")}
                    )

            if designator.user != request_user and designee.user != request_user:
                raise serializers.ValidationError(
                    {
                        "designee": _("위임인 또는 수임인에 작성자가 포함되어야 합니다."),
                        "designator": _("위임인 또는 수임인에 작성자가 포함되어야 합니다."),
                    }
                )
            if designator.user != request_user:
                if not request_user in designator.allowed_user.allowed_users.all():
                    raise serializers.ValidationError(
                        {"designator": _("위임장 작성을 위한 프로필 조회 허용을 확인해주세요.")}
                    )
                if "designator_signature" in data:
                    raise serializers.ValidationError({"signature-button": _("위임인만 서명이 가능합니다.")})
            if designator.user == designee.user:
                raise serializers.ValidationError({"designee": _("위임인과 수임인이 동일할 수 없습니다.")})
        except Profile.DoesNotExist:
            raise serializers.ValidationError({"detail": _("사용자가 존재하지 않습니다.")})
        return data

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop("address")
        designator = validated_data["designator"]
        designee = validated_data["designee"]
        allowedUser = AllowedUser.objects.get(profile=designator)
        if not designee in allowedUser.allowed_users.all():
            allowedUser.allowed_users.add(designee.user)
            allowedUser.save()

        address = Address.objects.create(**address_data)

        mandate = Mandate.objects.create(**validated_data, address=address)
        return mandate

    @transaction.atomic
    def update(self, instance, validated_data):
        address_data = validated_data.pop("address") if "address" in validated_data else {}

        address = instance.address
        for key, val in address_data.items():
            setattr(address, key, val)
        address.save()

        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        return instance
