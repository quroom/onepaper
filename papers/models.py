import os
import base64
from multiselectfield import MultiSelectField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from profiles.models import ExpertProfile, Profile, Insurance
from addresses.models import Address

class PaperStatus(models.Model):
    REQUESTING = 1
    DRAFT = 2
    PROGRESS = 3
    DONE = 4

    STATUS_CATEGORY = (
        (REQUESTING, _('요청중')),
        (DRAFT, _('작성중')),
        (PROGRESS, _('서명중')),
        (DONE, _('완료'))
    )

    status = models.PositiveSmallIntegerField(
        choices=STATUS_CATEGORY, default=DRAFT)

    def __str__(self):
        return str(self.status)

class Paper(models.Model):
    BUILDINGLAND = 7
    ETC = 100

    LAND_CATEGORY = (
        (BUILDINGLAND, _('대')),
        (ETC, _('기타'))
    )

    BUILDING_STRUCTURE = ()

    C1CNFACILITY = 70
    C2CNFACILITY = 71
    HOUSE = 80
    APARTMENT = 81
    ETC = 100

    BUILDING_CATEGORY = (
        (C1CNFACILITY, _('제1종근린생활시설')),
        (C2CNFACILITY, _('제2종근린생활시설')),
        (HOUSE, _('단독주택')),
        (APARTMENT, _('아파트')),
        (ETC, _('기타'))
    )

    # TR(TRADE) DL(Deposit Loan) RT(Rent) EX(Exchange) CS(Consulting)
    RENT = 1
    DEPOSITLOAN = 2
    PURCHASE = 3
    EXCAHNGE = 4
    TRADE_CATEGORY = (
        (RENT, _('월세')),
        (DEPOSITLOAN, _('전세')),
        (PURCHASE, _('매매')),
        (EXCAHNGE, _('교환')),
    )

    TELEVISION = 1
    REFRIGERATOR = 2
    WASHINGMACHINE = 3
    AIRCONDITIONER = 4
    BED = 5
    DESK = 6
    CLOSET = 7
    SHOECLOSET = 8
    GASRANGE = 9
    MICROWAVE = 10
    DOORLOCK = 11
    BIDET = 12
    ADDITIONALITEMS = 99
    OPTIONS_CATEGORY = (
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

    #FIXME Need to be moved to Realestates model.
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name="author_papers")
    land_category = models.PositiveSmallIntegerField(
        choices=LAND_CATEGORY, default=BUILDINGLAND)
    lot_area = models.FloatField(default=0, blank=True)
    building_structure = models.CharField(max_length=20, blank=True)
    building_category = models.PositiveSmallIntegerField(
        choices=BUILDING_CATEGORY, default=HOUSE, blank=True)
    building_area = models.FloatField(default=0, blank=True)
    trade_category = models.PositiveSmallIntegerField(
        choices=TRADE_CATEGORY, default=RENT)
    address = models.OneToOneField(Address,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name="paper")
    down_payment = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    security_deposit = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    monthly_fee = models.PositiveIntegerField(null=True, blank=True, default=0)
    maintenance_fee = models.PositiveIntegerField(null=True, blank=True, default=0)
    options = MultiSelectField(choices=OPTIONS_CATEGORY,
                            null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    special_agreement = models.TextField(blank=True)
    status = models.OneToOneField(
        PaperStatus,
        on_delete=models.CASCADE,
        related_name="paper"
    )

    class Meta:
        ordering = ['-updated_at']

class Contractor(models.Model):
    SELLER = 1
    BUYER = 2
    EXPERT = 3

    CONTRACTOR_CATEGORY = (
        (SELLER, _('임대인(매도인)')),
        (BUYER, _('임차인(매수인)')),
        (EXPERT, _('공인중개사'))
    )

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
    is_paper_hidden = models.BooleanField(default=False)
    is_allowed = models.BooleanField(default=False)

    group = models.PositiveSmallIntegerField(
        choices=CONTRACTOR_CATEGORY)
        
    class Meta:
        constraints = [
                        models.UniqueConstraint(fields=['profile', 'paper'],
                        name="unique_profile_paper")
                    ]

class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name="author_answers")
    body = models.TextField()
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name="contractor_answers")
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name="votes")

class ExplanationSignature(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    contractor = models.OneToOneField(Contractor,
                                      on_delete=models.CASCADE,
                                      related_name="explanation_signature")
    image = models.TextField()

    class Meta:
        ordering = ['-updated_at']

class Signature(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    contractor = models.OneToOneField(Contractor,
                                      on_delete=models.CASCADE,
                                      related_name="signature")
    image = models.TextField()

    def __str__(self):
        return str(self.contractor.profile.user)

    class Meta:
        ordering = ['-updated_at']

class VerifyingExplanation(models.Model):
    HOUSE = 1
    APARTMENT = 2
    PURCHASE = 3
    RENT = 4
    PAPER_CATEGORY = (
        (HOUSE, _('단독주택')),
        (APARTMENT, _('공동주택')),
        (PURCHASE, _('매매')),
        (RENT, _('임대'))
    )

    REGISTRATION_CERTIFICATE = 1
    CERTIFIED_COPY_OF_REGISTER = 2
    LAND_LEDGER = 3
    BUILDING_LEDGER = 4
    CADASTRAL_MAP = 5
    FOREST_LAND_CADASTRAL_MAP = 6
    CERTIFICATE_OF_LAND_USE_PLANNING = 7
    OTHERS = 99
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
    BUILDINGLAND = 7
    LAND_CATEGORY = (
        (BUILDINGLAND, _('대')),
    )

    C1CNFACILITY = 70
    C2CNFACILITY = 71
    HOUSE = 80
    APARTMENT = 81
    OTHERS = 99
    BUILDING_CATEGORY = (
        (C1CNFACILITY, _('제1종근린생활시설')),
        (C2CNFACILITY, _('제2종근린생활시설')),
        (HOUSE, _('단독주택')),
        (APARTMENT, _('아파트')),
        (OTHERS, _('기타'))
    )
    NONE = 0
    LONG_TERM = 1
    PUBLIC = 2
    OTHERS = 99

    RENTAL_HOUSING_REGISTRATION_CATEGORY = (
        (NONE, _('해당사항없음')),
        (LONG_TERM, _('장기일반민간임대주택')),
        (PUBLIC, _('공공지원민간임대주택')),
        (OTHERS, _('그 밖의 유형'))
    )

    LAND_SPECULATIVE_AREA = 1
    HOUSING_SPECULATIVE_AREA = 2
    SPECULATION_RIDDEN_DISTRICT = 3
    SPECULATIVE_AREA_CATEGORY = (
        (LAND_SPECULATIVE_AREA, _('토기투기지역')),
        (HOUSING_SPECULATIVE_AREA, _('주택투기지역')),
        (SPECULATION_RIDDEN_DISTRICT, _('투기과열지구'))
    )

    NONE = 0
    PRIVATE_PARKING = 1
    PUBLIC_PARKING = 2
    OTHERS = 99
    PARKING_LOT_CATEGORY = (
        (NONE, _('없음')),
        (PRIVATE_PARKING, _('전용주차시설')),
        (PUBLIC_PARKING, _('공동주차시설')),
        (OTHERS, _('그 밖의 주차시설'))
    )

    OUTSOURCING = 1
    SELF_MANAGEMENT = 2
    OTHERS = 99
    MANAGEMENT_CATEGORY = (
        (OUTSOURCING, _('위탁관리')),
        (SELF_MANAGEMENT, _('자체관리')),
        (OTHERS, _('그 밖의 유형'))
    )

    CENTRAL_SUPPLY = 1
    INDIVIDUAL_SUPPLY = 2
    HEATING_SUPPLY_CATEGORY = (
        (CENTRAL_SUPPLY, _('중앙공급')),
        (INDIVIDUAL_SUPPLY, _('개별공급'))
    )
    GAS = 1
    OIL = 2
    PROPANE_GAS = 3
    COAL_BRIQUETTES = 4
    OTHERS = 99
    HEATING_TYPE_CATEGORY = ((
        (GAS, _('도시가스')),
        (OIL, _('기름')),
        (PROPANE_GAS, _('프로판가스')),
        (COAL_BRIQUETTES, _('연탄')),
        (OTHERS, _('그밖의종류'))
    ))

    paper = models.OneToOneField(Paper,
                                on_delete=models.CASCADE,
                                related_name="verifying_explanation")
    insurance = models.ForeignKey(Insurance,
                                  on_delete=models.CASCADE,
                                  related_name="verifying_explanations")
    paper_categories = MultiSelectField(choices=PAPER_CATEGORY)
    explanation_evidences = MultiSelectField(choices=EXPLANATION_EVIDENCE_CATEGORY)
    explanation_evidence_info = models.CharField(max_length=15, blank=True)
    requesting_condition_info = models.CharField(max_length=120, blank=True)
    address = models.OneToOneField(Address,
                                   null=True,
                                   on_delete=models.SET_NULL)
    land_area = models.FloatField()
    ledger_land_category = models.PositiveSmallIntegerField(
        choices=LAND_CATEGORY, default=BUILDINGLAND)
    actual_land_category = models.PositiveSmallIntegerField(
        choices=LAND_CATEGORY, default=BUILDINGLAND)
    net_area = models.FloatField()
    land_share = models.CharField(max_length=12, blank=True)
    year_of_completion = models.SmallIntegerField()
    ledger_building_category = models.PositiveSmallIntegerField(
        choices=BUILDING_CATEGORY, default=HOUSE, blank=True)
    actual_building_category = models.PositiveSmallIntegerField(
        choices=BUILDING_CATEGORY, default=HOUSE, blank=True)
    building_structure = models.CharField(max_length=12)
    building_direction = models.CharField(max_length=15)
    seismic_design = models.CharField(max_length=12)
    seismic_capacity = models.CharField(max_length=12)
    legal_status = models.BooleanField()
    matters_of_violation = models.CharField(max_length=41, blank=True)
    land_ownership = models.CharField(max_length=30, blank=True)
    building_ownership = models.CharField(max_length=30, blank=True)
    land_other = models.CharField(max_length=30, blank=True)
    building_other = models.CharField(max_length=30, blank=True)
    rental_housing_registration = models.PositiveSmallIntegerField(choices=RENTAL_HOUSING_REGISTRATION_CATEGORY)
    rental_housing_registration_info = models.CharField(max_length=35, blank=True)
    mandatory_lease_period = models.PositiveSmallIntegerField(null=True, blank=True)
    lease_initiation_date = models.DateField(null=True, blank=True)
    right_to_lease_contract_renewal = models.BooleanField(null=True, blank=True, default=None)
    use_area = models.CharField(max_length=21, blank=True)
    use_district = models.CharField(max_length=21, blank=True)
    use_zone = models.CharField(max_length=21, blank=True)
    building_coverage_limit = models.PositiveSmallIntegerField(null=True, blank=True)
    floor_area_limit = models.PositiveSmallIntegerField(null=True, blank=True)
    planning_facilities = models.CharField(max_length=50, blank=True)
    permission_report_zone = models.BooleanField(null=True, blank=True)
    speculative_area = models.PositiveIntegerField(choices=SPECULATIVE_AREA_CATEGORY, null=True, blank=True)
    unit_planning_area_others = models.CharField(max_length=50, blank=True)
    other_use_restriction = models.CharField(max_length=22, blank=True)
    relative_with_roads = models.CharField(max_length=26)
    is_paved_rode = models.BooleanField()
    accessibility = models.BooleanField()
    bus_stop = models.CharField(max_length=15)
    bus_by_foot = models.BooleanField()
    bus_required_time = models.PositiveSmallIntegerField()
    subway_station = models.CharField(max_length=15, blank=True)
    subway_by_foot = models.BooleanField(null=True, blank=True)
    subway_required_time = models.PositiveSmallIntegerField(null=True, blank=True)
    parking_lot = models.PositiveSmallIntegerField(choices=PARKING_LOT_CATEGORY)
    parking_lot_info = models.CharField(max_length=10, blank=True)
    elementary_school = models.CharField(max_length=15)
    elementary_school_by_foot = models.BooleanField()
    elementary_school_required_time = models.PositiveSmallIntegerField()
    middle_school = models.CharField(max_length=15)
    middle_school_by_foot = models.BooleanField()
    middle_school_required_time = models.PositiveSmallIntegerField()
    high_school = models.CharField(max_length=15)
    high_school_by_foot = models.BooleanField()
    high_school_required_time = models.PositiveSmallIntegerField()
    department_store = models.CharField(max_length=15)
    department_store_by_foot = models.BooleanField()
    department_store_required_time = models.PositiveSmallIntegerField()
    medical_center = models.CharField(max_length=15)
    medical_center_by_foot = models.BooleanField()
    medical_center_required_time = models.PositiveSmallIntegerField()
    is_security_office = models.BooleanField()
    management = models.PositiveSmallIntegerField(choices=MANAGEMENT_CATEGORY)
    undesirable_facilities = models.BooleanField()
    undesirable_facilities_info = models.CharField(max_length=20,blank=True)
    expected_transaction_price = models.PositiveSmallIntegerField(null=True, blank=True)
    land_prcie_recorded = models.PositiveSmallIntegerField(null=True, blank=True)
    building_price_recorded = models.PositiveSmallIntegerField(null=True, blank=True)
    acquisition_tax = models.FloatField(null=True, blank=True)
    special_tax = models.FloatField(null=True, blank=True)
    local_education_tax = models.FloatField(null=True, blank=True)
    actual_legal_right_relationship = models.CharField(max_length=248, blank=True)
    water_damage_status = models.BooleanField()
    water_damage_status_info = models.CharField(max_length=25, blank=True)
    water_capacity_status = models.BooleanField()
    water_capacity_status_info = models.CharField(max_length=25, blank=True)
    electricity_supply_status = models.BooleanField()
    electricity_supply_status_info = models.CharField(max_length=20, blank=True)
    gas_supply_status = models.BooleanField()
    gas_supply_status_info = models.CharField(max_length=23, blank=True)
    is_fire_alarm_detector = models.BooleanField()
    fire_alarm_detector_quantity = models.PositiveSmallIntegerField(null=True, blank=True)
    heating_supply_method = models.PositiveSmallIntegerField(choices=HEATING_SUPPLY_CATEGORY)
    heating_status = models.BooleanField()
    heating_status_info = models.CharField(max_length=10, blank=True)
    heating_type = models.PositiveSmallIntegerField(choices=HEATING_TYPE_CATEGORY)
    heating_type_info = models.CharField(max_length=8, blank=True)
    is_elevator = models.BooleanField()
    elevator_status = models.BooleanField(null=True, blank=True)
    drainage_status = models.BooleanField()
    drainage_status_info = models.CharField(max_length=33, blank=True)
    other_facilities = models.CharField(max_length=69, blank=True)
    wall_crack_status = models.BooleanField()
    wall_crack_status_info = models.CharField(max_length=28, blank=True)
    water_leak_status = models.BooleanField()
    water_leak_status_info = models.CharField(max_length=28, blank=True)
    wall_paper_status = models.BooleanField(null=True)
    wall_paper_status_info = models.CharField(max_length=22, blank=True)
    sunshine_status = models.BooleanField(null=True)
    sunshine_status_info = models.CharField(max_length=40, blank=True)
    noise_status = models.BooleanField(null=True)
    vibration = models.BooleanField(null=True)
    comission = models.PositiveIntegerField()
    actual_expenses = models.PositiveIntegerField(blank=True)
    payment_period = models.CharField(max_length=200, blank=True)
    calculation_info = models.CharField(max_length=200, blank=True)
    additional_info = models.TextField(blank=True)