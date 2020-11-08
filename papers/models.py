import os
import base64
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from profiles.models import CustomUser, ExpertProfile, Profile
from addresses.models import Address

class Paper(models.Model):
    BUILDINGLAND = 7

    LAND_TYPE = (
        (BUILDINGLAND, _('대')),
    )

    BUILDING_STRUCTURE = ()

    C1CNFACILITY = 70
    C2CNFACILITY = 71
    HOUSE = 80
    APARTMENT = 81
    ETC = 100

    BUILDING_TYPE = (
        (C1CNFACILITY, _('제1종근린생활시설')),
        (C2CNFACILITY, _('제2종근린생활시설')),
        (HOUSE, _('단독주택')),
        (APARTMENT, _('아파트')),
        (ETC, _('기타'))
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
    land_type = models.PositiveSmallIntegerField(
        choices=LAND_TYPE, default=BUILDINGLAND, blank=True)
    lot_area = models.PositiveSmallIntegerField(default=0, blank=True)
    building_structure = models.CharField(max_length=100)
    building_type = models.PositiveSmallIntegerField(
        choices=BUILDING_TYPE, default=HOUSE, blank=True)
    building_area = models.SmallIntegerField(default=0, blank=True)
    trade_type = models.PositiveSmallIntegerField(
        choices=TRADE_TYPE, default=RENT, blank=True)
    address = models.OneToOneField(Address,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name="paper")
    room_name = models.CharField(max_length=50, blank=True)
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
        return self.address.old_address + ' ' + self.room_name + '-' + self.get_trade_type_display()

    class Meta:
        ordering = ['-id']
#Add unique profile+paper
class Contractor(models.Model):
    SELLER = 0
    BUYER = 1
    EXPERT = 2

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
       constraints = [
                     models.UniqueConstraint(fields=['profile', 'paper'],
                     name="unique_profile_paper")
                     ]
    
    def __str__(self):
        return str(self.profile.user)

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
        return str(self.contractor.profile.user)