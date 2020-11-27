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
        choices=LAND_TYPE, default=BUILDINGLAND)
    lot_area = models.FloatField(default=0, blank=True)
    building_structure = models.CharField(max_length=20)
    building_type = models.PositiveSmallIntegerField(
        choices=BUILDING_TYPE, default=HOUSE, blank=True)
    building_area = models.FloatField(default=0, blank=True)
    trade_type = models.PositiveSmallIntegerField(
        choices=TRADE_TYPE, default=RENT)
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

class VerifyingManual(models.Model):
    REGISTRATION_CERTIFICATE = 0
    CERTIFIED_COPY_OF_REGISTER = 1
    LAND_LEDGER = 2
    BUILDING_LEDGER = 3
    CADASTRAL_MAP = 4
    FOREST_LAND_CADASTRAL_MAP = 5
    CERTIFICATE_OF_LAND_USE_PLANNING = 6
    OTHERS = 7
    EXPLANATION_EVIDENCE_CATEGORY = (
        (REGISTRATION_CERTIFICATE, _('등기권리증')),
        (CERTIFIED_COPY_OF_REGISTER, _('등기사항증명서')),
        (LAND_LEDGER, _('토지대장')),
        (BUILDING_LEDGER, _('건축물대장')),
        (CADASTRAL_MAP, _('지적도')),
        (FOREST_LAND_CADASTRAL_MAP, _('임야도')),
        (CERTIFICATE_OF_LAND_USE_PLANNING, _('토지이용계획확인서')),
        (OTHERS, _('기타'))
    )
    HOUSE = 0
    APARTMENT = 1
    PURCHASE = 2
    RENT = 3
    PAPER_CATEGORY = (
        (HOUSE, _('단독주택')),
        (APARTMENT, _('공동주택')),
        (PURCHASE, _('매매')),
        (RENT, _('임대'))
    )
    BUILDINGLAND = 7
    LAND_CATEGORY = (
        (BUILDINGLAND, _('대')),
    )

    C1CNFACILITY = 70
    C2CNFACILITY = 71
    HOUSE = 80
    APARTMENT = 81
    OTHERS = 100
    BUILDING_CATEGORY = (
        (C1CNFACILITY, _('제1종근린생활시설')),
        (C2CNFACILITY, _('제2종근린생활시설')),
        (HOUSE, _('단독주택')),
        (APARTMENT, _('아파트')),
        (OTHERS, _('기타'))
    )
    LONG_TERM = 0
    PUBLIC = 1
    SHORT_TERM = 2
    NONE = 3

    RENTAL_HOUSING_REGISTRATION_CATEGORY = (
        (LONG_TERM, _('장기일반민간임대주택')),
        (PUBLIC, _('공공지원민간임대주택')),
        (SHORT_TERM, _('단기민간임대주택')),
        (NONE, _('해당사항없음'))
    )

    LAND_SPECULATIVE_AREA = 0
    HOUSING_SPECULATIVE_AREA = 1
    SPECULATION_RIDDEN_DISTRICT = 2
    SPECULATIVE_AREA_CATEGORY = (
        (LAND_SPECULATIVE_AREA, _('토기투기지역')),
        (HOUSING_SPECULATIVE_AREA, _('주택투기지역')),
        (SPECULATION_RIDDEN_DISTRICT, _('투기과열지구'))
    )

    NONE = 0
    PRIVATE_PARKING = 1
    PUBLIC_PARKING = 2
    OTHERS = 3    
    PARKING_LOT_CATEGORY = (
        (NONE, _('없음')),
        (PRIVATE_PARKING, _('전용주차시설')),
        (PUBLIC_PARKING, _('공동주차시설')),
        (OTHERS, _('그밖의주차시설'))
    )

    OUTSOURCING = 0
    SELF_MANAGEMENT = 1
    OTHERS = 2
    MANAGEMENT_CATEGORY = (
        (OUTSOURCING, _('위탁관리')),
        (SELF_MANAGEMENT, _('자체관리')),
        (OTHERS, _('그밖의유형'))
    )

    CENTRAL_SUPPLY = 0 
    INDIVIDUAL_SUPPLY = 1
    HEATING_SUPPLY_CATEGORY = (
        (CENTRAL_SUPPLY, _('중앙공급')),
        (INDIVIDUAL_SUPPLY, _('개별공급'))
    )
    GAS = 0
    OIL = 1
    PROPANE_GAS = 2
    COAL_BRIQUETTES = 3
    OTHERS = 4
    HEATING_TYPE_CATEGORY = ({
        (GAS, _('가스')),
        (OIL, _('기름')),
        (PROPANE_GAS, _('프로판가스')),
        (COAL_BRIQUETTES, _('연탄')),
        (OTHERS, _('그밖의종류'))
    })

    paper = models.OneToOneField(Paper,
                                on_delete=models.CASCADE,
                                related_name="verifying_manual")
    paper_category = MultiSelectField(choices=PAPER_CATEGORY)
    explanation_evidence = MultiSelectField(choices=EXPLANATION_EVIDENCE_CATEGORY)
    explanation_evidence_info = models.CharField(max_length=50, blank=True)
    address = models.OneToOneField(Address,
                                   null=True,
                                   on_delete=models.SET_NULL)
    land_area = models.FloatField()
    land_category = models.PositiveSmallIntegerField(
        choices=LAND_CATEGORY, default=BUILDINGLAND)
    land_actual_category = models.PositiveSmallIntegerField(
        choices=LAND_CATEGORY, default=BUILDINGLAND)
    net_area = models.FloatField()
    land_share = models.CharField(max_length=20)
    year_of_completion = models.DateField()
    building_category = models.PositiveSmallIntegerField(
        choices=BUILDING_CATEGORY, default=HOUSE, blank=True)
    building_actual_category = models.PositiveSmallIntegerField(
        choices=BUILDING_CATEGORY, default=HOUSE, blank=True)
    building_structure = models.CharField(max_length=20)
    building_direction = models.CharField(max_length=10)
    seismic_design = models.CharField(max_length=10)
    seismic_capacity = models.CharField(max_length=10)
    legal_status = models.BooleanField()
    matters_of_violation = models.CharField(max_length=50)
    land_ownership = models.CharField(max_length=100, blank=True)
    building_ownership = models.CharField(max_length=100, blank=True)
    land_other = models.CharField(max_length=100, blank=True)
    building_other = models.CharField(max_length=100, blank=True)
    rental_housing_registration = models.PositiveSmallIntegerField(choices=RENTAL_HOUSING_REGISTRATION_CATEGORY)
    use_area = models.CharField(max_length=20, blank=True)
    use_district = models.CharField(max_length=20, blank=True)
    use_zone = models.CharField(max_length=20, blank=True)
    building_coverage_limit = models.PositiveSmallIntegerField(blank=True)
    floor_area_limit = models.PositiveSmallIntegerField(blank=True)
    planning_facilities = models.CharField(max_length=20, blank=True)
    permission_report_zone = models.BooleanField(blank=True)
    speculative_area = models.PositiveIntegerField(choices=SPECULATIVE_AREA_CATEGORY, blank=True)
    unit_planning_area_others = models.CharField(max_length=20, blank=True)
    other_use_restriction = models.CharField(max_length=20, blank=True)
    relative_with_roads = models.CharField(max_length=20)
    aacessibility = models.BooleanField()
    bus_stop = models.CharField(max_length=20)
    bus_by_foot = models.BooleanField()
    bus_time_required = models.PositiveSmallIntegerField()
    subway_station = models.CharField(max_length=20)
    subway_by_foot = models.BooleanField()
    subway_time_required = models.PositiveSmallIntegerField()
    parking_lot = models.PositiveSmallIntegerField(choices=PARKING_LOT_CATEGORY)
    parking_lot_info = models.CharField(max_length=10, blank=True)
    elementary_school = models.CharField(max_length=20)
    elementary_school_by_foot = models.BooleanField()
    elementary_school_time_required = models.PositiveSmallIntegerField()
    middle_school = models.CharField(max_length=20)
    middle_school_by_foot = models.BooleanField()
    middle_school_time_required = models.PositiveSmallIntegerField()
    high_school = models.CharField(max_length=20)
    high_school_by_foot = models.BooleanField()
    high_school_time_required = models.PositiveSmallIntegerField()
    department_store = models.CharField(max_length=20)
    department_store_by_foot = models.BooleanField()
    department_store_time_required = models.PositiveSmallIntegerField()
    medical_center = models.CharField(max_length=20)
    medical_center_by_foot = models.BooleanField()
    medical_center_time_required = models.PositiveSmallIntegerField()
    security_office = models.BooleanField()
    management = models.PositiveSmallIntegerField(choices=MANAGEMENT_CATEGORY)
    undesirable_facilities = models.BooleanField()
    undesirable_facilities_info = models.CharField(max_length=50,blank=True)
    expected_transaction_price = models.PositiveSmallIntegerField(blank=True)
    land_prcie_recorded = models.PositiveSmallIntegerField(blank=True)
    buildling_price_recorded = models.PositiveSmallIntegerField(blank=True)
    acquisition_tax = models.FloatField(blank=True)
    special_tax = models.FloatField(blank=True)
    local_education_tax = models.FloatField(blank=True)
    water_damage_status = models.BooleanField()
    water_damage_location = models.CharField(max_length=20, blank=True)
    water_capacity_status = models.BooleanField()
    water_capacity_location = models.CharField(max_length=20, blank=True)
    electricity_supply_status = models.BooleanField()
    electricity_location = models.CharField(max_length=20, blank=True)
    gas_supply_status = models.BooleanField()
    gas_supply_info = models.CharField(max_length=20, blank=True)
    fire_alarm_detector = models.BooleanField()
    fire_alarm_detector_quantity = models.PositiveSmallIntegerField(blank=True)
    heating_supply_method = models.PositiveSmallIntegerField(choices=HEATING_SUPPLY_CATEGORY)
    heating_status = models.BooleanField()
    heating_status_info = models.CharField(max_length=20, blank=True)
    heating_type = models.PositiveSmallIntegerField(choice=HEATING_TYPE_CATEGORY)
    heating_type_info = models.CharField(max_length=20, blank=True)
    is_elevator = models.BooleanField()
    elevator_status = models.BooleanField(blank=True)
    drainage_status = models.BooleanField()
    drainage_status_info = models.CharField(max_length=20, blank=True)
    other_facilities = models.CharField(max_length=50)
    wall_crack_status = models.BooleanField()
    wall_crack_status_info = models.CharField(max_length=20, blank=True)
    water_leak_status = models.BooleanField()
    water_leak_status_info = models.CharField(max_length=20, blank=True)
    wall_paper_status = models.NullBooleanField()
    wall_paper_status_info = models.CharField(max_length=20, blank=True)
    sunshine_status = models.NullBooleanField()
    sunshine_status_info = models.CharField(max_length=20, blank=True)
    noise_status = models.NullBooleanField()
    vibration = models.NullBooleanField()
    comission = models.PositiveIntegerField()
    actual_expenses = models.PositiveIntegerField(blank=True)
    payment_period = models.DateField()
    caculation_info = models.TextField()

class ManualSignature(models.Model):
    contractor = models.OneToOneField(Contractor,
                                      on_delete=models.CASCADE,
                                      related_name="explanation_signature")
    image = models.ImageField()

    def __str__(self):
        return str(self.contractor.profile.user)