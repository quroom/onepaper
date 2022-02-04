from typing import List

from django.conf import settings
from django.db import models
from django.db.models.fields import related

from addresses.models import Address
from core.models import Comment
from papers.models import Paper


# Reference. https://github.com/alvinshaita/django-realestate/blob/master/listings/models.py
# Create your models here.
class Listing(models.Model):
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
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="author_listings",
    )
    content = models.TextField(blank=True)
    item_category = models.PositiveSmallIntegerField(choices=ITEM_CATEGORY, default=ONEROOM)
    title = models.CharField(max_length=25, blank=True)
    trade_category = models.PositiveSmallIntegerField(
        choices=Paper.TRADE_CATEGORY, default=Paper.RENT
    )
    online_visit = models.BooleanField(default=True)
    short_lease = models.BooleanField(default=False)
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
