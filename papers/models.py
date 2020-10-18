import os
import base64
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from profiles.models import CustomUser, ExpertProfile, Profile

class Paper(models.Model):
    ONEROOM = 0
    TWOROOM = 1
    THREEROOM = 2
    FOURROOM = 3
    SHAREHOUSE = 4
    OFFICETEL = 5

    APARTMENT = 20
    VILLA = 21
    HOUSE = 22
    COMMERCIALHOUSE = 23

    STORE = 40
    LAND = 41
    ITEM_TYPE = (
        (ONEROOM, _('원룸')),
        (TWOROOM, _('투룸')),
        (THREEROOM, _('쓰리룸')),
        (FOURROOM, _('포룸')),
        (SHAREHOUSE, _('쉐어하우스')),
        (OFFICETEL, _('오피스텔')),

        (APARTMENT, _('아파트')),
        (VILLA, _('빌라')),
        (HOUSE, _('단독주택')),
        (COMMERCIALHOUSE, _('상가주택')),

        (STORE, _('상가')),
        (LAND, _('토지')),
    )

    # TR(TRADE) DL(Deposit Loan) RT(Rent) EX(Exchange) CS(Consulting)
    RENT = 0
    DEPOSITLOAN = 1
    TRADE = 2
    EXCAHNGE = 3
    TRADE_TYPE = (
        (RENT, _('월세')),
        (DEPOSITLOAN, _('전세')),
        (TRADE, _('매매')),
        (EXCAHNGE, _('교환')),
    )

    DRAFT = 0
    DONE = 1
    CONFIRMED = 2
    HIDDEN = 3

    STATUS_TYPE = (
        (DRAFT, _('작성중')),
        (DONE, _('작성완료')),
        (CONFIRMED, _('확인완료')),
        (HIDDEN, _('숨김'))
    )

    # Need to be moved to Realestates model.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser,
                               null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name="author_papers")
    land_type = models.CharField(max_length=10)
    lot_area = models.PositiveSmallIntegerField(default=0, blank=True)
    building_structure = models.CharField(max_length=100)
    building_type = models.CharField(max_length=100)
    building_area = models.SmallIntegerField(default=0, blank=True)
    trade_type = models.PositiveSmallIntegerField(
        choices=TRADE_TYPE, default=RENT, blank=True)
    address = models.CharField(max_length=250)
    room_name = models.CharField(max_length=50, blank=True)
    realestate_type = models.PositiveSmallIntegerField(
        choices=ITEM_TYPE, default=ONEROOM, blank=True)
    down_payment = models.BigIntegerField(null=True, blank=True)
    security_deposit = models.BigIntegerField(null=True, blank=True)
    monthly_fee = models.PositiveIntegerField(null=True, blank=True)
    maintenance_fee = models.PositiveIntegerField(null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    special_agreement = models.TextField(blank=True)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_TYPE, default=DRAFT)

    def __str__(self):
        return self.address + ' ' + self.room_name + '-' + self.get_trade_type_display()

#Add unique profile+paper
class Contractor(models.Model):
    SELLER = 1
    BUYER = 2
    EXPERT = 3

    CONTRACTOR_TYPE = (
        (SELLER, _('임대인(매도인)')),
        (BUYER, _('임차인(매수인)')),
        (EXPERT, _('공인중개사'))
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name="profile_contractors",
                                related_query_name="profile_contractors")
    paper = models.ForeignKey(Paper,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name="paper_contractors",
                              related_query_name="paper_contractors")
    group = models.PositiveSmallIntegerField(
        choices=CONTRACTOR_TYPE)
        
    class Meta:
        unique_together = ('paper', 'profile')

from django.conf import settings
class Signature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paper_visible = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    contractor = models.OneToOneField(Contractor,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True,
                                      related_name="signature")
    image = models.ImageField()
    def __str__(self):
        return str(self.user)