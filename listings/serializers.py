from django.core.files.images import get_image_dimensions
from django.db import transaction
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from listings.models import Listing, ListingAddress, ListingImage, ListingStatus
from onepaper.serializers import ReadOnlyModelSerializer
from profiles.serializers import (
    ListingEveryoneExpertProfileSerializer,
    ListingEveryoneProfileSerializer,
)


class ListingStatusSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = ListingStatus
        fields = ["status"]


class ListingAddressSerializer(ModelSerializer):
    class Meta:
        model = ListingAddress
        exclude = ("listing",)


class ListingImageSerializer(ModelSerializer):
    is_deleted = serializers.BooleanField(required=False, default=False)
    id = serializers.IntegerField(required=False)
    image = serializers.FileField(required=False)

    class Meta:
        model = ListingImage
        exclude = ("listing",)


class ListingEveryoneSerializer(ReadOnlyModelSerializer):
    author_profile = serializers.SerializerMethodField()
    listingaddress = serializers.SerializerMethodField()
    images = ListingImageSerializer(source="listingimage_set", many=True, required=False)
    status = serializers.IntegerField(source="listingstatus.status", required=False)

    class Meta:
        model = Listing
        exclude = ["author"]

    def get_author_profile(self, instance):
        author = instance.author
        if author.is_expert:
            return ListingEveryoneExpertProfileSerializer(
                author.profiles.filter(is_activated=True).first()
            ).data
        else:
            return ListingEveryoneProfileSerializer(
                author.profiles.filter(is_activated=True).first()
            ).data

    def get_listingaddress(self, instance):
        address_with_bun = instance.listingaddress.old_address.split("-")[0]
        hidden_address = (
            address_with_bun[0 : address_with_bun.rindex(" ")]
            if address_with_bun.find(" ") != -1
            else ""
        )
        old_address_eng = instance.listingaddress.old_address_eng
        hidden_address_eng = (
            old_address_eng[old_address_eng.index(" ") + 1 : len(old_address_eng)]
            if old_address_eng.find(" ") != -1
            else ""
        )
        return {"old_address": hidden_address, "old_address_eng": hidden_address_eng}

    def get_status(self, instance):
        return instance.listingstatus.status


class ListingSerializer(ModelSerializer):
    author_profile = serializers.SerializerMethodField()
    images = ListingImageSerializer(source="listingimage_set", many=True, required=False)
    listingaddress = ListingAddressSerializer()
    status = serializers.IntegerField(source="listingstatus.status", required=False)

    class Meta:
        model = Listing
        exclude = ["author"]

    def validate(self, data):
        images_data = data.get("listingimage_set")
        is_default_image_updated = False
        if self.instance != None:
            total_images = ListingImage.objects.filter(listing=self.instance)
            total_images_count = total_images.count()
            if images_data != None:
                images_data_count = len(images_data)
                deleted_images_count = 0
                for image_data in images_data:
                    if image_data.get("is_deleted") == True:
                        deleted_images_count += 1
                    if image_data.get("is_default") == True:
                        id = image_data.get("id")
                        if total_images.filter(id=id).exists():
                            is_default_image_updated = True
                total_images_count = (
                    total_images_count
                    - deleted_images_count
                    + (images_data_count - deleted_images_count)
                )
        else:
            total_images_count = len(images_data) if images_data != None else 0
        total_images_count = (
            total_images_count - 1 if is_default_image_updated else total_images_count
        )

        if total_images_count > 10:
            raise serializers.ValidationError({"image": _("이미지는 10개까지 첨부할 수 있습니다.")})

        if images_data != None:
            for image_data in images_data:
                image = image_data.get("image")
                if image != None:
                    width, height = get_image_dimensions(image)
                    if width > 1024 or height > 1024:
                        raise serializers.ValidationError(
                            {"image": _("이미지 해상도 초과입니다. 최대 1024x1024까지 지원합니다.")}
                        )
        return data

    def get_author_profile(self, instance):
        author = instance.author
        if author.is_expert:
            return ListingEveryoneExpertProfileSerializer(
                author.profiles.filter(is_activated=True).first()
            ).data
        else:
            return ListingEveryoneProfileSerializer(
                author.profiles.filter(is_activated=True).first()
            ).data

    def get_status(self, instance):
        return instance.listingstatus.status

    @transaction.atomic
    def create(self, validated_data):
        if not validated_data.get("listingimage_set") is None:
            images_data = validated_data.pop("listingimage_set")
        else:
            raise serializers.ValidationError({"detail": _("하나 이상의 이미지를 첨부하여야 합니다.")})

        address_data = validated_data.pop("listingaddress")
        listing = Listing.objects.create(**validated_data)
        ListingAddress.objects.create(listing=listing, **address_data)
        ListingStatus.objects.create(listing=listing)

        for image_data in images_data:
            image = image_data.get("image")
            is_default = image_data.get("is_default")
            ListingImage.objects.create(listing=listing, image=image, is_default=is_default)

        # Delete image code.
        return listing

    @transaction.atomic
    def update(self, instance, validated_data):
        images_data = (
            validated_data.pop("listingimage_set")
            if not validated_data.get("listingimage_set") is None
            else {}
        )
        listingaddress = instance.listingaddress
        listingaddress_data = (
            validated_data.pop("listingaddress")
            if not validated_data.get("listingaddress") is None
            else {}
        )

        for key, val in listingaddress_data.items():
            setattr(listingaddress, key, val)
        listingaddress.save()

        for image_data in images_data:
            img_id = image_data.get("id")
            is_default = image_data.get("is_default")
            is_deleted = image_data.get("is_deleted")
            if is_default:
                ListingImage.objects.filter(listing=instance, is_default=True).update(
                    is_default=False
                )
            if img_id != None:
                try:
                    if is_deleted:
                        ListingImage.objects.get(id=img_id).delete()
                    elif is_default:
                        ListingImage.objects.filter(listing=instance, is_default=True).update(
                            is_default=False
                        )
                        listingimage = ListingImage.objects.get(id=img_id)
                        listingimage.is_default = True
                        listingimage.save()
                except ListingImage.DoesNotExist:
                    raise serializers.ValidationError(
                        {"detail": _("존재하지 않는 이미지(ID:%(id)d)입니다.") % {"id": img_id}}
                    )
            else:
                image = image_data.get("image")
                ListingImage.objects.create(listing=instance, image=image, is_default=is_default)

        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()

        return instance
