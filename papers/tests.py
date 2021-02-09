import datetime
import tempfile
import os

from django.utils.translation import ugettext_lazy as _
from PIL import Image
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from addresses.models import Address
from profiles.models import AllowedUser, CustomUser, Profile, ExpertProfile
from papers.models import Paper, PaperStatus

address_vars = {
            "old_address": '광주 광산구 명도동 169',
            "old_address_eng": '169, Myeongdo-dong, Gwangsan-gu, Gwangju, Korea',
            "new_address": '광주광역시 광산구 가마길 2-21',
            "bjdongName": "명도동",
            "bjdongName_eng": "Myeongdo-dong",
            "sigunguCd": '29200',
            "bjdongCd": '29200',
            "platGbCd": '',
            "bun":'169',
            "ji":'',
            "dong":'',
            "ho":'2층',
}

address_form = {
        "address.old_address": "서울 강동구 성내동 111-39",
        "address.old_address_eng": '111-39, Seongnae-dong, Gangdong-gu, Seoul, Korea',
        "address.new_address": "서울 강동구 풍성로 87-14",
        "address.bjdongName": "성내동",
        "address.bjdongName_eng": "Seongnae-dong",
        "address.sigunguCd": '11740',
        "address.bjdongCd": '11740',
        "address.platGbCd": '',
        "address.bun":'111',
        "address.ji":'39',
        "address.dong":'',
        "address.ho":'2층',
}

# Create your tests here.
class PaperTestCase(APITestCase):
    list_url = reverse("papers-list")
    profile_list_url = reverse("profiles-list")
    verifying_explanation = {
                "accessibility": True,
                "acquisition_tax": None,
                "actual_building_category": 80,
                "actual_expenses": 50000,
                "actual_land_category": 7,
                "address": address_vars,
                "building_category": 80,
                "building_coverage_limit": None,
                "building_direction": "남향  (기준:  )",
                "building_other": "",
                "building_ownership": "",
                "building_price_recorded": None,
                "building_structure": "철근콘크리트",
                "bus_by_foot": True,
                "bus_required_time": 5,
                "bus_stop": "전남대후문",
                "calculation_info": "<산출내역> ↵↵중개보수: ↵실    비: ↵※ 중개보수는 시ㆍ도 조례로 정한 요율에 따르거나, 시ㆍ도 조례로 정한 요율한도에서 중개의뢰인과 개업공인중개사가 서로 협의하여 결정하도록 한 요율에 따르며 부가가치세는 별도로 부과될 수 있습니다.",
                "comission": 2000000,
                "department_store": "홈플러스",
                "department_store_by_foot": False,
                "department_store_required_time": 10,
                "drainage_status": True,
                "drainage_status_info": "",
                "electricity_supply_status": True,
                "electricity_supply_status_info": "",
                "elementary_school": "중흥초등",
                "elementary_school_by_foot": True,
                "elementary_school_required_time": 10,
                "elevator_status": None,
                "expected_transaction_price": None,
                "explanation_evidence_info": "",
                "explanation_evidences": [],
                "fire_alarm_detector_quantity": None,
                "floor_area_limit": None,
                "gas_supply_status": True,
                "gas_supply_status_info": "",
                "heating_status": True,
                "heating_status_info": "",
                "heating_supply_method": 1,
                "heating_type": 0,
                "heating_type_info": "",
                "high_school": "전남대사범대학부설고등",
                "high_school_by_foot": True,
                "high_school_required_time": 10,
                "id": 28,
                "is_elevator": False,
                "is_fire_alarm_detector": False,
                "is_paved_rode": True,
                "is_security_office": False,
                "land_area": 55,
                "land_category": 7,
                "land_other": "",
                "land_ownership": "",
                "land_prcie_recorded": None,
                "land_share": "",
                "legal_status": True,
                "local_education_tax": None,
                "management": 1,
                "matters_of_violation": "",
                "medical_center": "전남대병원",
                "medical_center_by_foot": False,
                "medical_center_required_time": 20,
                "middle_school": "전대사범대학부설중",
                "middle_school_by_foot": True,
                "middle_school_required_time": 10,
                "net_area": 50,
                "noise_status": True,
                "other_facilities": "",
                "other_use_restriction": "",
                "paper": 54,
                "paper_categories": [],
                "parking_lot": 0,
                "parking_lot_info": "",
                "payment_period": "",
                "permission_report_zone": None,
                "planning_facilities": "",
                "relative_with_roads": "( 4m × 2m ) 도로에 접함",
                "rental_housing_registration": 3,
                "requesting_condition_info": "",
                "seismic_capacity": "해당사항없음",
                "seismic_design": "해당사항없음",
                "special_tax": None,
                "speculative_area": None,
                "subway_by_foot": False,
                "subway_required_time": 10,
                "subway_station": "상무",
                "sunshine_status": True,
                "sunshine_status_info": "",
                "undesirable_facilities": False,
                "undesirable_facilities_info": "",
                "unit_planning_area_others": "",
                "use_area": "",
                "use_district": "",
                "use_zone": "",
                "vibration": True,
                "wall_crack_status": False,
                "wall_crack_status_info": "",
                "wall_paper_status": True,
                "wall_paper_status_info": "",
                "water_capacity_status": True,
                "water_capacity_status_info": "",
                "water_damage_status": False,
                "water_damage_status_info": "",
                "water_leak_status": False,
                "water_leak_status_info": "",
                "year_of_completion": 1995
            }
    def api_authentication(self, user):
        self.token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test",
                                                   email="test@naver.com",
                                                   password="some_strong_password",
                                                   bio="bio",
                                                   name="김주영",
                                                   birthday="1955-02-12")
        address = Address.objects.create(**address_vars)
        self.profile = Profile.objects.create(user=self.user, address=address, bank_name="광주은행",
        account_number="120982711", mobile_number="010-1234-5678")

        user1 = CustomUser.objects.create_user(username="test9",
                                                   email="test9@naver.com",
                                                   password="some_strong_password",
                                                   bio="bio",
                                                   name="김주영",
                                                   birthday="1955-02-12")
        address = Address.objects.create(**address_vars)
        self.profile1 = Profile.objects.create(user=user1, address=address, bank_name="국민은행",
        account_number="120982711", mobile_number="010-3456-7890")

        expert_user = CustomUser.objects.create_user(username="expert",
                                            email="expert@naver.com",
                                            password="some_strong_password",
                                            bio="bio",
                                            name="서주은",
                                            birthday="1955-02-12",
                                            is_expert=True)
        address = Address.objects.create(**address_vars)
        profile2 = Profile.objects.create(user=expert_user, address=address, bank_name="충북은행", account_number="1111111", mobile_number="010-3982-5555")
        self.expert_profile = ExpertProfile.objects.create(profile=profile2, registration_number="2020118181-11", shop_name="효암중개사")
        self.expert_profile.status = ExpertProfile.APPROVED
        self.expert_profile.save()

        profile_allowed_user = AllowedUser.objects.create(profile=self.profile)
        profile_allowed_user.allowed_users.add(self.user)
        profile_allowed_user.allowed_users.add(expert_user)
        profile_allowed_user1 = AllowedUser.objects.create(profile=self.profile1)
        profile_allowed_user1.allowed_users.add(self.user)
        profile_allowed_user1.allowed_users.add(expert_user)
        expert_profile_allowed_user = AllowedUser.objects.create(profile=self.expert_profile.profile)
        expert_profile_allowed_user.allowed_users.add(self.user)

        self.api_authentication(self.user)
        self.create_profile()

    def create_profile(self):
        data = {
            "mobile_number": "010-1234-1234",
            "bank_name": "국민은행",
            "account_number": "94334292963",
            **address_form
        }
        response = self.client.post(self.profile_list_url, data=data)
        return response

    def create_user_profile(self, id=0, is_expert=False):
        user = CustomUser.objects.create_user(username="test"+str(id), email="test@naver.com", password="some_strong_password",
                                              bio="bio", name="김주영", birthday="1955-02-12")
        if is_expert:
            user.is_expert=True
            user.save()
        address = Address.objects.create(**address_vars)
        profile = Profile.objects.create(user=user, address=address, bank_name="국민은행", account_number="98373737372", mobile_number="010-9827-111"+str(id))
        AllowedUser.objects.create(profile=profile)
        if is_expert:
            expert_profile = ExpertProfile.objects.create(
                profile=profile, registration_number="2020118181-11", shop_name="효암중개사")
            return expert_profile
        return profile

    def test_paper_create(self):
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
                {"profile": self.profile1.id, "paper": None, "group": "1"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"],  PaperStatus.DRAFT)

    def test_paper_create_without_self_profile(self):
        profile2 = self.create_user_profile(id=2)
        profile2_allowed_user = AllowedUser.objects.get(profile=profile2)
        profile2_allowed_user.allowed_users.add(self.user)
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": profile2.id, "paper": None, "group": "0"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["seller"][0], _("작성자가 포함되지 않았습니다."))
        self.assertEqual(response.data["buyer"][0], _("작성자가 포함되지 않았습니다."))

    def test_paper_create_with_same_profiles(self):
        response = self.create_profile()

        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
                {"profile": response.data['id'], "paper": None, "group": "1"}
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['buyer'][0], _("같은 회원을 중복해서 등록할 수 없습니다."))

    def test_paper_create_with_expert(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
                {"profile": self.profile1.id, "paper": None, "group": "1"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
            "verifying_explanation": self.verifying_explanation
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"],  PaperStatus.DRAFT)

    def test_paper_create_with_expert_unallowed_paper_requsting_status(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        profile2 = self.create_user_profile(id=2)
        
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
                {"profile": profile2.id, "paper": None, "group": "1"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
            "verifying_explanation": self.verifying_explanation
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"],  PaperStatus.REQUESTING)

        #AllowPaperTest
        forbidden_response = self.client.get(reverse('allow-paper', kwargs={'pk':response.data['paper_contractors'][1]['id']}))
        self.assertEqual(forbidden_response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=profile2.user)
        response = self.client.get(reverse('allow-paper', kwargs={'pk':response.data['paper_contractors'][1]['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"],  PaperStatus.DRAFT)
        response = self.client.get(reverse('allow-paper', kwargs={'pk':response.data['paper_contractors'][1]['id']}))
        self.assertEqual(response.data["detail"].message, _("이미 계약서 작성이 허용 되었습니다."))

    def test_paper_create_with_expert_as_trader(self):
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "1"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["buyer"][0], _("공인중개사는 거래자로 등록할 수 없습니다."))

    def test_paper_create_with_unapproved_expert(self):
        expert_profile = self.create_user_profile(id=1, is_expert=True)
        expert_profile_allowed_user = AllowedUser.objects.get(profile=expert_profile.profile)
        expert_profile_allowed_user.allowed_users.add(self.user)
        self.api_authentication(user=expert_profile.profile.user)

        profile2 = self.create_user_profile(id=2)
        profile2_allowed_user = AllowedUser.objects.get(profile=profile2)
        profile2_allowed_user.allowed_users.add(expert_profile.profile.user)
        profile_allowed_user = AllowedUser.objects.get(profile=self.profile)
        profile_allowed_user.allowed_users.add(expert_profile.profile.user)
        
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
                {"profile": profile2.id, "paper": None, "group": "1"},
                {"profile": expert_profile.profile.id, "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["expert"][0], _("공인중개사로 승인되지 않은 사용자는 계약서에 등록할 수 없습니다."))
    
    def test_paper_create_with_expert_without_verifying_explnation(self):
        self.api_authentication(user=self.expert_profile.profile.user)

        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
                {"profile": self.profile1.id, "paper": None, "group": "1"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["verifying_explanation"][0], _("작성자가 공인중개사인 경우 확인설명서를 비워둘 수 없습니다."))
    
    def test_paper_create_with_expert_without_expert(self):
        self.api_authentication(user=self.expert_profile.profile.user)
        
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
                {"profile": self.profile1.id, "paper": None, "group": "1"}
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["expert"][0], _("작성자가 공인중개사인 경우 비워둘 수 없습니다."))

    def test_paper_update(self):
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"}
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 99,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"}
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.put(reverse('papers-detail', kwargs={'pk':response.data['id']}), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lot_area'], 99)

    def test_paper_update_with_paperstatus_done(self):
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"}
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 99,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"}
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        paper_status = Paper.objects.get(id=1).status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        response = self.client.put(reverse('papers-detail', kwargs={'pk':response.data['id']}), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("완료된 계약서는 수정할 수 없습니다."))

    def test_paper_delete(self):
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        response = self.client.delete(reverse('papers-detail', kwargs={'pk':response.data['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_paper_delete_with_paperstatus_done(self):
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"}
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        paper_status = Paper.objects.get(id=1).status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        response = self.client.delete(reverse('papers-detail', kwargs={'pk':response.data['id']}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("완료된 계약서는 삭제할 수 없습니다."))

    def test_verifying_explanation_create(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        data ={
            "address": address_vars,
            "building_area": 22,
            "building_category": 80,
            "building_structure": "222",
            "down_payment": 50,
            "from_date": "2020-12-24",
            "land_category": 7,
            "lot_area": 222,
            "maintenance_fee": 0,
            "monthly_fee": 20,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "2"}
            ],
            "security_deposit": 1000,
            "special_agreement": "<p>ㅎㅎ</p>",
            "to_date": "2020-12-31",
            "trade_category": 0,
            "verifying_explanation": self.verifying_explanation
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.put(reverse('papers-detail', kwargs={'pk': response.data['id']}), data={
            "verifying_explanation": {
                "accessibility": False,
            }
        }, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(reverse('papers-detail', kwargs={'pk': response.data['id']}), data={
            "verifying_explanation": {
                "water_capacity_status": False,
            }
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['verifying_explanation']['water_capacity_status'], False)

    #FIXME: ADD verifying_explanation testcode.

MEDIA_ROOT = tempfile.mkdtemp()
@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class SignatureTestCase(APITestCase):
    list_url = reverse("papers-list")

    def _create_image(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            image = Image.new("RGB", (200, 200), "white")
            image.save(f, 'PNG')
        return open(f.name, mode='rb')

    def api_authentication(self, user):
        self.token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def setUp(self):
        self.image = self._create_image()
        self.image1 = self._create_image()
        self.image2 = self._create_image()
        self.image3 = self._create_image()
        self.image4 = self._create_image()
        self.image5 = self._create_image()
        expert_user = CustomUser.objects.create_user(username="expert",
                                                    email="expert@naver.com",
                                                    password="some_strong_password",
                                                    bio="bio",
                                                    name="서주은",
                                                    birthday="1955-02-12",
                                                    is_expert=True)
        address = Address.objects.create(**address_vars)
        profile2 = Profile.objects.create(user=expert_user, address=address, bank_name="충북은행", account_number="1111111", mobile_number="010-3982-5555")
        self.expert_profile = ExpertProfile.objects.create(profile=profile2, registration_number="2020118181-11", shop_name="효암중개사")
        self.expert_profile.status = ExpertProfile.APPROVED
        self.expert_profile.save()
        self.user = CustomUser.objects.create_user(username="test",
                                                    email="test@naver.com",
                                                    password="some_strong_password",
                                                    bio="bio",
                                                    name="김주영",
                                                    birthday="1955-02-12")
        self.api_authentication(user=self.user)
        address = Address.objects.create(**address_vars)
        self.profile = Profile.objects.create(user=self.user, address=address, bank_name="국민은행", account_number="1908281111", mobile_number="010-3982-1111")
        profile_allowed_user = AllowedUser.objects.create(profile=self.profile)
        profile_allowed_user.allowed_users.add(self.expert_profile.profile.user)
        user = CustomUser.objects.create_user(username="test1",
                                                    email="test1@naver.com",
                                                    password="some_strong_password",
                                                    bio="bio",
                                                    name="김길동",
                                                    birthday="1955-02-12")
        address = Address.objects.create(**address_vars)
        self.profile1 = Profile.objects.create(user=user, address=address, bank_name="서울은행", account_number="1111111", mobile_number="010-3982-2222")
        profile1_allowed_user = AllowedUser.objects.create(profile=self.profile1)
        profile1_allowed_user.allowed_users.add(self.user)
        profile_allowed_user.allowed_users.add(self.expert_profile.profile.user)
        address = Address.objects.create(**address_vars)
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
                {"profile": self.profile1.id, "paper": None, "group": "1"}
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        self.paper = self.client.post(self.list_url, data=data, format="json").data
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        data = {
            "address": address_vars,
            "building_area": 1111,
            "building_category": 80,
            "building_structure": "11",
            "down_payment": 1111,
            "from_date": "2020-11-18",
            "land_category": 7,
            "lot_area": 11,
            "maintenance_fee": 111,
            "monthly_fee": None,
            "options": [0, 1, 2],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "0"},
                {"profile": self.profile1.id, "paper": None, "group": "1"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "2"}
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
            'verifying_explanation': {
                    "accessibility": True,
                    "acquisition_tax": None,
                    "actual_building_category": 80,
                    "actual_expenses": 50000,
                    "actual_land_category": 7,
                    "address": address_vars,
                    "building_category": 80,
                    "building_coverage_limit": None,
                    "building_direction": "남향  (기준:  )",
                    "building_other": "",
                    "building_ownership": "",
                    "building_price_recorded": None,
                    "building_structure": "철근콘크리트",
                    "bus_by_foot": True,
                    "bus_required_time": 5,
                    "bus_stop": "전남대후문",
                    "calculation_info": "<산출내역> ↵↵중개보수: ↵실    비: ↵※ 중개보수는 시ㆍ도 조례로 정한 요율에 따르거나, 시ㆍ도 조례로 정한 요율한도에서 중개의뢰인과 개업공인중개사가 서로 협의하여 결정하도록 한 요율에 따르며 부가가치세는 별도로 부과될 수 있습니다.",
                    "comission": 2000000,
                    "department_store": "홈플러스",
                    "department_store_by_foot": False,
                    "department_store_required_time": 10,
                    "drainage_status": True,
                    "drainage_status_info": "",
                    "electricity_supply_status": True,
                    "electricity_supply_status_info": "",
                    "elementary_school": "중흥초등",
                    "elementary_school_by_foot": True,
                    "elementary_school_required_time": 10,
                    "elevator_status": None,
                    "expected_transaction_price": None,
                    "explanation_evidence_info": "",
                    "explanation_evidences": [],
                    "fire_alarm_detector_quantity": None,
                    "floor_area_limit": None,
                    "gas_supply_status": True,
                    "gas_supply_status_info": "",
                    "heating_status": True,
                    "heating_status_info": "",
                    "heating_supply_method": 1,
                    "heating_type": 0,
                    "heating_type_info": "",
                    "high_school": "전남대사범대학부설고등",
                    "high_school_by_foot": True,
                    "high_school_required_time": 10,
                    "id": 28,
                    "is_elevator": False,
                    "is_fire_alarm_detector": False,
                    "is_paved_rode": True,
                    "is_security_office": False,
                    "land_area": 55,
                    "land_category": 7,
                    "land_other": "",
                    "land_ownership": "",
                    "land_prcie_recorded": None,
                    "land_share": "",
                    "legal_status": True,
                    "local_education_tax": None,
                    "management": 1,
                    "matters_of_violation": "",
                    "medical_center": "전남대병원",
                    "medical_center_by_foot": False,
                    "medical_center_required_time": 20,
                    "middle_school": "전대사범대학부설중",
                    "middle_school_by_foot": True,
                    "middle_school_required_time": 10,
                    "net_area": 50,
                    "noise_status": True,
                    "other_facilities": "",
                    "other_use_restriction": "",
                    "paper": 54,
                    "paper_categories": [],
                    "parking_lot": 0,
                    "parking_lot_info": "",
                    "payment_period": "",
                    "permission_report_zone": None,
                    "planning_facilities": "",
                    "relative_with_roads": "( 4m × 2m ) 도로에 접함",
                    "rental_housing_registration": 3,
                    "requesting_condition_info": "",
                    "seismic_capacity": "해당사항없음",
                    "seismic_design": "해당사항없음",
                    "special_tax": None,
                    "speculative_area": None,
                    "subway_by_foot": False,
                    "subway_required_time": 10,
                    "subway_station": "상무",
                    "sunshine_status": True,
                    "sunshine_status_info": "",
                    "undesirable_facilities": False,
                    "undesirable_facilities_info": "",
                    "unit_planning_area_others": "",
                    "use_area": "",
                    "use_district": "",
                    "use_zone": "",
                    "vibration": True,
                    "wall_crack_status": False,
                    "wall_crack_status_info": "",
                    "wall_paper_status": True,
                    "wall_paper_status_info": "",
                    "water_capacity_status": True,
                    "water_capacity_status_info": "",
                    "water_damage_status": False,
                    "water_damage_status_info": "",
                    "water_leak_status": False,
                    "water_leak_status_info": "",
                    "year_of_completion": 1995
                }
            }
        self.paper_with_verifying_explanation = self.client.post(self.list_url, data=data, format="json").data
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.image.close()
        os.remove(self.image.name)
        self.image1.close()
        os.remove(self.image1.name)
        self.image2.close()
        os.remove(self.image2.name)
        self.image3.close()
        os.remove(self.image3.name)
        self.image4.close()
        os.remove(self.image4.name)
        self.image5.close()
        os.remove(self.image5.name)
    
    def test_explanation_signature_create(self):
        data = {
            'contractor': self.paper_with_verifying_explanation['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-explanation-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_explanation_signature_create_unauthorization(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        data = {
            'contractor': self.paper_with_verifying_explanation['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-explanation-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_explanation_signature_create_with_paper_done(self):
        data = {
            'contractor': self.paper_with_verifying_explanation['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)
        response = self.client.post(reverse('create-explanation-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.client.force_authenticate(user=self.profile1.user)
        data = {
            'contractor': self.paper_with_verifying_explanation['paper_contractors'][1]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)
        response = self.client.post(reverse('create-explanation-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        data = {
            'contractor': self.paper_with_verifying_explanation['paper_contractors'][2]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)
        response = self.client.post(reverse('create-explanation-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.get(reverse('papers-detail', kwargs={'pk':self.paper_with_verifying_explanation['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], PaperStatus.DONE)

    def test_explanation_signature_create_after_paper_done(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        paper = Paper.objects.get(id=2)
        paper_status = paper.status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        response = self.client.post(reverse('create-explanation-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("계약서 작성이 완료되어 서명을 추가할 수 없습니다."))

    def test_explanation_signature_create_duplications(self):
        data = {
            'contractor': self.paper_with_verifying_explanation['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        self.client.post(reverse('create-explanation-signature', kwargs={'id':self.paper['id']}), data)
        response = self.client.post(reverse('create-explanation-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("이미 서명이 등록되어있습니다."))

    def test_explanation_signature_update(self):
        data = {
            'contractor': self.paper_with_verifying_explanation['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-explanation-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)

        data = {
            'contractor': self.paper_with_verifying_explanation['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.put(reverse('update-explanation-signature', kwargs={'paper_id':self.paper_with_verifying_explanation['id'], 'pk':response.data['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_explanation_signature_update_after_paper_done(self):
        data = {
            'contractor': self.paper_with_verifying_explanation['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-explanation-signature', kwargs={'id':self.paper_with_verifying_explanation['id']}), data)
        paper = Paper.objects.get(id=2)
        paper_status = paper.status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        data = {
            'contractor': self.paper_with_verifying_explanation['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.put(reverse('update-explanation-signature', kwargs={'paper_id':paper.id, 'pk':response.data['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("완료된 계약서의 서명은 수정할 수 없습니다."))

    def test_signature_create(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signature_create_unauthorization(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_signature_create_with_paper_done(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.client.force_authenticate(user=self.profile1.user)
        data = {
            'contractor': self.paper['paper_contractors'][1]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('papers-detail', kwargs={'pk':self.paper['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], PaperStatus.DONE)

    def test_signature_create_after_paper_done(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        paper = Paper.objects.get(id=1)
        paper_status = paper.status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("계약서 작성이 완료되어 서명을 추가할 수 없습니다."))

    def test_signature_create_duplications(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("이미 서명이 등록되어있습니다."))

    def test_signature_update(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)

        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.put(reverse('update-signature', kwargs={'paper_id':self.paper['id'], 'pk':response.data['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signature_update_after_paper_done(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        paper = Paper.objects.get(id=1)
        paper_status = paper.status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d"
        }
        response = self.client.put(reverse('update-signature', kwargs={'paper_id':paper.id, 'pk':response.data['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("완료된 계약서의 서명은 수정할 수 없습니다."))