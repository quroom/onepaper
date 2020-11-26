import os
import base64
from multiselectfield import MultiSelectField
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from profiles.models import CustomUser, ExpertProfile, Profile
from addresses.models import Address

class PaperStatus(models.Model):
    DRAFT = 0
    PROGRESS = 1
    DONE = 2

    STATUS_TYPE = (
        (DRAFT, _('작성중')),
        (PROGRESS, _('서명중')),
        (DONE, _('완료'))
    )

    status = models.PositiveSmallIntegerField(
        choices=STATUS_TYPE, default=DRAFT)

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

    TELEVISION = 0
    REFRIGERATOR = 1
    WASHINGMACHINE = 2
    AIRCONDITIONER = 3
    BED = 4
    DESK = 5
    CLOSET = 6
    SHOECLOSET = 7
    GASRANGE = 8
    MICROWAVE = 9
    DOORLOCK = 10
    BIDET = 11
    ADDITIONALITEMS = 99
    OPTIONS_TYPE = (
        (TELEVISION, _('티비')),
        (REFRIGERATOR, _('냉장고')),
        (WASHINGMACHINE, _('세탁기')),
        (AIRCONDITIONER, _('에어컨')),
        (BED, _('침대')),
        (DESK, _('책상')),
        (CLOSET, _('옷장')),
        (SHOECLOSET, _('신발장')),
        (GASRANGE, _('가스렌지')),
        (MICROWAVE, _('전자렌지')),
        (DOORLOCK, _('도어락')),
        (BIDET, _('비데')),
        (ADDITIONALITEMS, _('추가물품')),
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
    lot_area = models.FloatField(default=0, blank=True)
    building_structure = models.CharField(max_length=100)
    building_type = models.PositiveSmallIntegerField(
        choices=BUILDING_TYPE, default=HOUSE, blank=True)
    building_area = models.FloatField(default=0, blank=True)
    trade_type = models.PositiveSmallIntegerField(
        choices=TRADE_TYPE, default=RENT, blank=True)
    address = models.OneToOneField(Address,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name="paper")

    down_payment = models.BigIntegerField(null=True, blank=True)
    security_deposit = models.BigIntegerField(null=True, blank=True)
    monthly_fee = models.PositiveIntegerField(null=True, blank=True)
    maintenance_fee = models.PositiveIntegerField(null=True, blank=True)
    options = MultiSelectField(choices=OPTIONS_TYPE,
                            null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    special_agreement = models.TextField(blank=True)
    status = models.OneToOneField(
        PaperStatus,
        on_delete=models.CASCADE,
        related_name="paper"
    )

    def __str__(self):
        return self.address.old_address + ' ' + self.address.ho + ' ' + self.address.ho + '-' + self.get_trade_type_display()

    class Meta:
        ordering = ['-updated_at']

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
                                on_delete=models.CASCADE,
                                related_name="profile_contractors",
                                related_query_name="profile_contractors")
    paper = models.ForeignKey(Paper,
                              blank=True,
                              null=True,
                              on_delete=models.CASCADE,
                              related_name="paper_contractors",
                              related_query_name="paper_contractors")
    is_paper_visible = models.BooleanField(default=True)
    group = models.PositiveSmallIntegerField(
        choices=CONTRACTOR_TYPE)
        
    class Meta:
       constraints = [
                     models.UniqueConstraint(fields=['profile', 'paper'],
                     name="unique_profile_paper")
                     ]
    
    def __str__(self):
        return str(self.profile.user)

class Signature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contractor = models.OneToOneField(Contractor,
                                      on_delete=models.CASCADE,
                                      related_name="signature")
    image = models.ImageField()
    def __str__(self):
        return str(self.contractor.profile.user)

    class Meta:
        ordering = ['-updated_at']

class VerifyingExplanation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paper = models.OneToOneField(Paper,
                                on_delete=models.CASCADE,
                                related_name="verifying_explanation")
    pdf = models.FileField()

    class Meta:
        ordering = ['-updated_at']    

class ExplanationSignature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contractor = models.OneToOneField(Contractor,
                                      on_delete=models.CASCADE,
                                      related_name="explanation_signature")
    image = models.ImageField()

    def __str__(self):
        return str(self.contractor.profile.user)

    class Meta:
        ordering = ['-updated_at']