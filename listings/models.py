from typing import List

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from addresses.models import Address
from core.models import Comment
from papers.models import Paper


class ListingConstant:
    ONEROOM = 1
    TWOROOM = 2
    THREEROOM = 3
    FOURROOM = 4
    SHAREHOUSE = 5
    OFFICETEL = 6

    APARTMENT = 20
    VILLA = 21
    HOUSE = 22
    COMMERCIALHOUSE = 23

    STORE = 40
    LAND = 41

    ECT = 99
    ITEM_CATEGORY = (
        (ONEROOM, "원룸"),
        (TWOROOM, "투룸"),
        (THREEROOM, "쓰리룸"),
        (FOURROOM, "포룸"),
        (SHAREHOUSE, "쉐어하우스"),
        (OFFICETEL, "오피스텔"),
        (APARTMENT, "아파트"),
        (VILLA, "빌라"),
        (HOUSE, "단독주택"),
        (COMMERCIALHOUSE, "상가주택"),
        (STORE, "상가"),
        (LAND, "토지"),
        (ECT, "기타"),
    )


class AskListing(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="author_asklistings",
    )
    location = models.CharField(max_length=25, blank=True)
    online_visit = models.BooleanField(default=True)
    term_of_lease = models.SmallIntegerField(default=12)
    item_category = models.PositiveSmallIntegerField(
        choices=ListingConstant.ITEM_CATEGORY, default=ListingConstant.ONEROOM
    )
    trade_category = models.PositiveSmallIntegerField(
        choices=Paper.TRADE_CATEGORY, default=Paper.RENT
    )
    security_deposit = models.PositiveBigIntegerField(blank=True, default=0)
    monthly_fee = models.PositiveIntegerField(blank=True, default=0)
    maintenance_fee = models.PositiveIntegerField(blank=True, default=0)
    visit_date = models.DateField(null=True, blank=True)
    moving_date = models.DateField(null=True, blank=True)
    content = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]


# Reference. https://github.com/alvinshaita/django-realestate/blob/master/listings/models.py
class Listing(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="author_listings",
    )
    content = models.TextField(blank=True)
    item_category = models.PositiveSmallIntegerField(
        choices=ListingConstant.ITEM_CATEGORY, default=ListingConstant.ONEROOM
    )
    title = models.CharField(max_length=25, blank=True)
    trade_category = models.PositiveSmallIntegerField(
        choices=Paper.TRADE_CATEGORY, default=Paper.RENT
    )
    online_visit = models.BooleanField(default=True)
    # FIXME: Remove short_lease after minimum_period
    minimum_period = models.PositiveSmallIntegerField(default=12, null=True)
    short_lease = models.BooleanField(default=False, blank=True, null=True)
    # FIXME: Remove null True
    down_payment = models.PositiveBigIntegerField(blank=True, default=0)
    security_deposit = models.PositiveBigIntegerField(blank=True, default=0)
    monthly_fee = models.PositiveIntegerField(blank=True, default=0)
    maintenance_fee = models.PositiveIntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # FIXME: Add listing status like full or not.
    class Meta:
        ordering = ["-updated_at"]


# FIXME: 입주문의 남기면 코멘트 남게끔 구현.
class ListingComment(Comment):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)
    image = models.ImageField()
    # FIXME: Remove Null True
    is_default = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ["-is_default", "id"]


class ListingAddress(Address):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)


class ListingStatus(models.Model):
    FULL = 0
    AVALIABLE = 1

    STATUS_CATEGORY = (
        (FULL, _("만실")),
        (AVALIABLE, _("가능")),
    )

    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUS_CATEGORY, default=AVALIABLE)

    def __str__(self):
        return str(self.status)
