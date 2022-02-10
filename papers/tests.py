import os
import tempfile
from datetime import timedelta

from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from addresses.models import Address
from papers.models import Paper, PaperStatus, Signature
from profiles.models import AllowedUser, CustomUser, ExpertProfile, Insurance, Profile

today = timezone.localtime().date()
address_vars = {
    "old_address": "광주 광산구 명도동 169",
    "old_address_eng": "169, Myeongdo-dong, Gwangsan-gu, Gwangju, Korea",
    "new_address": "광주광역시 광산구 가마길 2-21",
    "bjdongName": "명도동",
    "bjdongName_eng": "Myeongdo-dong",
    "sigunguCd": "29200",
    "bjdongCd": "29200",
    "platGbCd": "",
    "bun": "169",
    "ji": "",
    "dong": "",
    "ho": "2층",
}

address_form = {
    "address.old_address": "서울 강동구 성내동 111-39",
    "address.old_address_eng": "111-39, Seongnae-dong, Gangdong-gu, Seoul, Korea",
    "address.new_address": "서울 강동구 풍성로 87-14",
    "address.bjdongName": "성내동",
    "address.bjdongName_eng": "Seongnae-dong",
    "address.sigunguCd": "11740",
    "address.bjdongCd": "11740",
    "address.platGbCd": "",
    "address.bun": "111",
    "address.ji": "39",
    "address.dong": "",
    "address.ho": "2층",
}

# Create your tests here.
class PaperTestCase(APITestCase):
    list_url = reverse("papers-list")
    profile_list_url = reverse("profiles-list")
    verifying_explanation = {
        "accessibility": True,
        "acquisition_tax": None,
        "actual_building_category": "단독주택",
        "actual_expenses": 50000,
        "actual_land_category": 7,
        "address": address_vars,
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
        "floor_surface_status": 1,
        "floor_surface_status_info": "",
        "gas_supply_status": True,
        "gas_supply_status_info": "",
        "heating_status": True,
        "heating_status_info": "",
        "heating_supply_method": 1,
        "heating_type": 1,
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
        "ledger_building_category": "단독주택",
        "legal_status": True,
        "local_education_tax": None,
        "management": 2,
        "matters_of_violation": "",
        "medical_center": "전남대병원",
        "medical_center_by_foot": False,
        "medical_center_required_time": 20,
        "middle_school": "전대사범대학부설중",
        "middle_school_by_foot": True,
        "middle_school_required_time": 10,
        "multi_family_housing_document": None,
        "net_area": 50,
        "noise_status": 1,
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
        "rental_housing_registration": 2,
        "rental_housing_registration_info": "",
        "requesting_condition_info": "",
        "right_to_lease_contract_renewal": None,
        "seismic_capacity": "해당사항없음",
        "seismic_design": "해당사항없음",
        "special_tax": None,
        "speculative_area": None,
        "subway_by_foot": False,
        "subway_required_time": 10,
        "subway_station": "상무",
        "sunshine_status": 1,
        "sunshine_status_info": "",
        "undesirable_facilities": False,
        "undesirable_facilities_info": "",
        "unit_planning_area_others": "",
        "use_area": "",
        "use_district": "",
        "use_zone": "",
        "vibration": 1,
        "wall_crack_status": False,
        "wall_crack_status_info": "",
        "wall_paper_status": 1,
        "wall_paper_status_info": "",
        "water_capacity_status": True,
        "water_capacity_status_info": "",
        "water_damage_status": False,
        "water_damage_status_info": "",
        "water_leak_status": False,
        "water_leak_status_info": "",
        "year_of_completion": 1995,
    }

    def _create_image(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            image = Image.new("RGB", (200, 200), "white")
            image.save(f, "PNG")

        return open(f.name, mode="rb")

    def api_authentication(self, user):
        self.token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email="test@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
        )
        address = Address.objects.create(**address_vars)
        cls.profile = Profile.objects.create(
            user=cls.user,
            address=address,
            bank_name=34,
            account_number="120982711",
            mobile_number="010-1234-5678",
        )

        user1 = CustomUser.objects.create_user(
            email="test9@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
        )
        address = Address.objects.create(**address_vars)
        cls.profile1 = Profile.objects.create(
            user=user1,
            address=address,
            bank_name=4,
            account_number="120982711",
            mobile_number="010-3456-7890",
        )

        expert_user = CustomUser.objects.create_user(
            email="expert@naver.com",
            password="some_strong_password",
            bio="bio",
            name="서주은",
            birthday="1955-02-12",
            is_expert=True,
        )
        address = Address.objects.create(**address_vars)
        profile2 = Profile.objects.create(
            user=expert_user,
            address=address,
            bank_name=7,
            account_number="1111111",
            mobile_number="010-3982-5555",
        )
        cls.expert_profile = ExpertProfile.objects.create(
            profile=profile2, registration_number="2020118181-11", shop_name="효암중개사"
        )
        Insurance.objects.create(
            expert_profile=cls.expert_profile,
            from_date=today,
            to_date=today.replace(year=today.year + 1),
        )
        cls.expert_profile.status = ExpertProfile.APPROVED
        cls.expert_profile.save()

        profile_allowed_user = AllowedUser.objects.create(profile=cls.profile)
        profile_allowed_user.allowed_users.add(cls.user)
        profile_allowed_user.allowed_users.add(expert_user)
        profile_allowed_user1 = AllowedUser.objects.create(profile=cls.profile1)
        profile_allowed_user1.allowed_users.add(cls.user)
        profile_allowed_user1.allowed_users.add(expert_user)
        expert_profile_allowed_user = AllowedUser.objects.create(
            profile=cls.expert_profile.profile
        )
        expert_profile_allowed_user.allowed_users.add(cls.user)
        address = Address.objects.create(**address_vars)
        Profile.objects.create(
            user=cls.user,
            address=address,
            bank_name=4,
            account_number="98373737372",
            mobile_number="010-9827-111" + str(id),
        )

    def setUp(self):
        self.image = self._create_image()
        self.api_authentication(self.user)

    # FIXME: remove files and folders also profile test file too.
    def tearDown(self):
        self.image.close()
        os.remove(self.image.name)

    def create_profile(self):
        data = {
            "mobile_number": "010-1234-1234",
            "bank_name": 4,
            "account_number": "94334292963",
            **address_form,
        }
        response = self.client.post(self.profile_list_url, data=data)
        return response

    def create_user_profile(self, id=0, is_expert=False):
        user = CustomUser.objects.create_user(
            email="test" + str(id) + "@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
        )
        if is_expert:
            user.is_expert = True
            user.save()
        address = Address.objects.create(**address_vars)
        profile = Profile.objects.create(
            user=user,
            address=address,
            bank_name=4,
            account_number="98373737372",
            mobile_number="010-9827-111" + str(id),
        )
        AllowedUser.objects.create(profile=profile)
        if is_expert:
            today = timezone.localtime().date()
            expert_profile = ExpertProfile.objects.create(
                profile=profile, registration_number="2020118181-11", shop_name="효암중개사"
            )
            Insurance.objects.create(
                expert_profile=expert_profile,
                from_date=today,
                to_date=today.replace(year=today.year + 1),
            )
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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.profile1.id, "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], PaperStatus.DRAFT)

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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": profile2.id, "paper": None, "group": "1"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": response.data["id"], "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["buyer"][0], _("같은 회원을 중복해서 등록할 수 없습니다."))

    def test_paper_create_with_expert(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        self.verifying_explanation["insurance"] = self.expert_profile.insurances.first().id
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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.profile1.id, "paper": None, "group": "2"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "3"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
            "verifying_explanation": self.verifying_explanation,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], PaperStatus.DRAFT)

    def test_paper_create_with_expert_unallowed_paper_and_allow_hide_paper(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        profile2 = self.create_user_profile(id=2)
        self.verifying_explanation["insurance"] = self.expert_profile.insurances.first().id

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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": profile2.id, "paper": None, "group": "2"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "3"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
            "verifying_explanation": self.verifying_explanation,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        paper_id = response.data["id"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], PaperStatus.REQUESTING)

        # AllowPaperTest Forbidden
        forbidden_response = self.client.put(
            reverse("allow-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_allowed": True},
            format="json",
        )
        self.assertEqual(forbidden_response.status_code, status.HTTP_403_FORBIDDEN)

        forbidden_response = self.client.put(
            reverse("hide-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_hidden": True},
            format="json",
        )
        self.assertEqual(forbidden_response.status_code, status.HTTP_403_FORBIDDEN)

        # authenticate for authorized user.
        self.client.force_authenticate(user=profile2.user)

        # HidePaperTest
        response_error = self.client.put(
            reverse("hide-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_hidden": True},
            format="json",
        )
        self.assertEqual(response_error.data["detail"].message, _("완료 또는 거절된 계약서만 숨김 처리가 가능합니다."))

        # AllowPaperTest
        response = self.client.put(
            reverse("allow-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_allowed": True},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["paper_contractors"][1]["is_allowed"], True)
        self.assertEqual(response.data["status"], PaperStatus.DRAFT)

        response_error = self.client.put(
            reverse("allow-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_allowed": True},
            format="json",
        )
        self.assertEqual(response_error.data["detail"].message, _("이미 계약서 작성이 허용 되었습니다."))

        response = self.client.put(
            reverse("allow-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_allowed": False},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["paper_contractors"][1]["is_allowed"], False)
        self.assertEqual(response.data["status"], PaperStatus.DENIED)

        response_error = self.client.put(
            reverse("allow-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_allowed": False},
            format="json",
        )
        self.assertEqual(response_error.data["detail"].message, _("이미 계약서 작성이 거절 되었습니다."))

        response_error = self.client.put(
            reverse("allow-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={},
            format="json",
        )
        self.assertEqual(response_error.data["detail"].message, _("요청 데이터가 올바르지 않습니다."))

        # HidePaperTest
        response = self.client.put(
            reverse("hide-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_hidden": True},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["paper_contractors"][1]["is_hidden"], True)

        # AllowPaperTest
        response_error = self.client.put(
            reverse("allow-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_allowed": True},
            format="json",
        )
        self.assertEqual(
            response_error.data["detail"].message,
            _("숨김 처리된 계약서는 승인/거절이 불가합니다. 계약서 보임 처리 후 재요청 해주세요."),
        )

        # HidePaperTest
        response_error = self.client.put(
            reverse("hide-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_hidden": True},
            format="json",
        )
        self.assertEqual(response_error.data["detail"].message, _("이미 계약서가 숨김 처리 되었습니다."))

        response = self.client.put(
            reverse("hide-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_hidden": False},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["paper_contractors"][1]["is_hidden"], False)

        response_error = self.client.put(
            reverse("hide-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_hidden": False},
            format="json",
        )
        self.assertEqual(response_error.data["detail"].message, _("이미 계약서가 보임 처리 되었습니다."))

        response_error = self.client.put(
            reverse("hide-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={},
            format="json",
        )
        self.assertEqual(response_error.data["detail"].message, _("요청 데이터가 올바르지 않습니다."))

        # AllowPaperTest with DONE Paper
        paper = Paper.objects.get(id=paper_id)
        paper_status = paper.status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        response_error = self.client.put(
            reverse("allow-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_allowed": False},
            format="json",
        )
        self.assertEqual(response_error.data["detail"].message, _("서명 또는 완료된 계약서는 거절할 수 없습니다."))

        paper_status = paper.status
        paper_status.status = PaperStatus.PROGRESS
        paper_status.save()
        response_error = self.client.put(
            reverse("allow-paper", kwargs={"pk": response.data["paper_contractors"][1]["id"]}),
            data={"is_allowed": False},
            format="json",
        )
        self.assertEqual(response_error.data["detail"].message, _("서명 또는 완료된 계약서는 거절할 수 없습니다."))

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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": profile2.id, "paper": None, "group": "2"},
                {"profile": expert_profile.profile.id, "paper": None, "group": "3"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["expert"][0], _("승인 및 활성화되지 않은 공인중개사 프로필은 계약서에 등록할 수 없습니다.")
        )

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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.profile1.id, "paper": None, "group": "2"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "3"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["verifying_explanation"][0], _("작성자가 공인중개사인 경우 확인설명서를 비워둘 수 없습니다.")
        )

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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.profile1.id, "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
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
            "options": [1, 2, 3],
            "paper_contractors": [{"profile": self.profile.id, "paper": None, "group": "1"}],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
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
            "options": [1, 2, 3],
            "paper_contractors": [{"profile": self.profile.id, "paper": None, "group": "1"}],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.put(
            reverse("papers-detail", kwargs={"pk": response.data["id"]}), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["lot_area"], 99)

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
            "options": [1, 2, 3],
            "paper_contractors": [{"profile": self.profile.id, "paper": None, "group": "1"}],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
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
            "options": [1, 2, 3],
            "paper_contractors": [{"profile": self.profile.id, "paper": None, "group": "1"}],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        paper_status = Paper.objects.get(id=1).status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        response = self.client.put(
            reverse("papers-detail", kwargs={"pk": response.data["id"]}), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("완료 또는 거절된 계약서는 수정할 수 없습니다."))

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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        response = self.client.delete(reverse("papers-detail", kwargs={"pk": response.data["id"]}))
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
            "options": [1, 2, 3],
            "paper_contractors": [{"profile": self.profile.id, "paper": None, "group": "1"}],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        paper_status = Paper.objects.get(id=1).status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        response = self.client.delete(reverse("papers-detail", kwargs={"pk": response.data["id"]}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("완료된 계약서는 삭제할 수 없습니다."))

    def test_insurance_update(self):
        self.api_authentication(user=self.expert_profile.profile.user)
        data = {
            "from_date": today.replace(year=today.year - 1),
            "to_date": today.replace(year=today.year + 2),
        }
        response = self.client.patch(
            reverse(
                "profile-insurances-detail",
                kwargs={
                    "profile_pk": self.expert_profile.profile.id,
                    "pk": self.expert_profile.insurances.first().id,
                },
            ),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_insurance_update_invalid_date(self):
        self.api_authentication(user=self.expert_profile.profile.user)
        self.verifying_explanation["insurance"] = self.expert_profile.insurances.first().id
        data = {
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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "3"},
            ],
            "security_deposit": 1000,
            "special_agreement": "<p>ㅎㅎ</p>",
            "title": "테스트",
            "to_date": "2020-12-31",
            "trade_category": 1,
            "verifying_explanation": self.verifying_explanation,
        }
        response = self.client.post(self.list_url, data=data, format="json")

        data = {
            "from_date": today.replace(year=today.year - 1),
            "to_date": today.replace(year=today.year + 1),
        }

        response = self.client.patch(
            reverse(
                "profile-insurances-detail",
                kwargs={
                    "profile_pk": self.expert_profile.profile.id,
                    "pk": self.expert_profile.insurances.first().id,
                },
            ),
            {},
        )
        self.assertEqual(response.data["detail"].message, _("보증서류 시작일과 종료일을 모두 입력해주세요."))

        response = self.client.patch(
            reverse(
                "profile-insurances-detail",
                kwargs={
                    "profile_pk": self.expert_profile.profile.id,
                    "pk": self.expert_profile.insurances.first().id,
                },
            ),
            data,
        )
        self.assertEqual(
            response.data["detail"].message, _("보증서류가 포함된 거래계약서가 있는 경우 보증서류 시작일을 변경할 수 없습니다.")
        )

    def test_used_insurance_delete(self):
        self.api_authentication(user=self.expert_profile.profile.user)
        self.verifying_explanation["insurance"] = self.expert_profile.insurances.first().id
        data = {
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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "3"},
            ],
            "security_deposit": 1000,
            "special_agreement": "<p>ㅎㅎ</p>",
            "title": "테스트",
            "to_date": "2020-12-31",
            "trade_category": 1,
            "verifying_explanation": self.verifying_explanation,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        response = self.client.delete(
            reverse(
                "profile-insurances-detail",
                kwargs={
                    "profile_pk": self.expert_profile.profile.id,
                    "pk": self.expert_profile.insurances.first().id,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"].message, _("보증서류가 포함된 거래계약서가 있는 경우 보증서류 정보를 삭제할 수 없습니다.")
        )

    def test_verifying_explanation_create(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        self.verifying_explanation["insurance"] = self.expert_profile.insurances.first().id
        data = {
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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "3"},
            ],
            "security_deposit": 1000,
            "special_agreement": "<p>ㅎㅎ</p>",
            "title": "테스트",
            "to_date": "2020-12-31",
            "trade_category": 1,
            "verifying_explanation": self.verifying_explanation,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.put(
            reverse("papers-detail", kwargs={"pk": response.data["id"]}),
            data={
                "verifying_explanation": {
                    "accessibility": False,
                }
            },
            format="json",
        )
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(
            reverse("papers-detail", kwargs={"pk": response.data["id"]}),
            data={
                "verifying_explanation": {
                    "water_capacity_status": False,
                }
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["verifying_explanation"]["water_capacity_status"], False)

    def test_verifying_explanation_create_without_insurance(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        data = {
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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "3"},
            ],
            "security_deposit": 1000,
            "special_agreement": "<p>ㅎㅎ</p>",
            "title": "테스트",
            "to_date": "2020-12-31",
            "trade_category": 1,
            "verifying_explanation": self.verifying_explanation,
        }
        response = self.client.post(self.list_url, data=data, format="json")

        expert_profile = self.create_user_profile(id=1, is_expert=True)
        data["verifying_explanation"]["insurance"] = expert_profile.insurances.first().id

        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["insurance"][0], _("보유하지 않은 중개보증서류가 추가되었습니다."))

    # FIXME: ADD verifying_explanation testcode.


MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class SignatureTestCase(APITestCase):
    list_url = reverse("papers-list")

    def _create_image(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            image = Image.new("RGB", (200, 200), "white")
            image.save(f, "PNG")
        return open(f.name, mode="rb")

    def api_authentication(self, user):
        self.token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        expert_user = CustomUser.objects.create_user(
            email="expert@naver.com",
            password="some_strong_password",
            bio="bio",
            name="서주은",
            birthday="1955-02-12",
            is_expert=True,
        )
        address = Address.objects.create(**address_vars)
        profile2 = Profile.objects.create(
            user=expert_user,
            address=address,
            bank_name=2,
            account_number="1111111",
            mobile_number="010-3982-5555",
        )
        cls.expert_profile = ExpertProfile.objects.create(
            profile=profile2, registration_number="2020118181-11", shop_name="효암중개사"
        )
        Insurance.objects.create(
            expert_profile=cls.expert_profile,
            from_date=today,
            to_date=today.replace(year=today.year + 1),
        )
        cls.expert_profile.status = ExpertProfile.APPROVED
        cls.expert_profile.save()
        cls.user = CustomUser.objects.create_user(
            email="test@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
        )
        address = Address.objects.create(**address_vars)
        cls.profile = Profile.objects.create(
            user=cls.user,
            address=address,
            bank_name=4,
            account_number="1908281111",
            mobile_number="010-3982-1111",
        )
        profile_allowed_user = AllowedUser.objects.create(profile=cls.profile)
        profile_allowed_user.allowed_users.add(cls.expert_profile.profile.user)
        user = CustomUser.objects.create_user(
            email="test1@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김길동",
            birthday="1955-02-12",
        )
        address = Address.objects.create(**address_vars)
        cls.profile1 = Profile.objects.create(
            user=user,
            address=address,
            bank_name=7,
            account_number="1111111",
            mobile_number="010-3982-2222",
        )
        profile1_allowed_user = AllowedUser.objects.create(profile=cls.profile1)
        profile1_allowed_user.allowed_users.add(cls.user)
        profile_allowed_user.allowed_users.add(cls.expert_profile.profile.user)
        address = Address.objects.create(**address_vars)

    def setUp(self):
        self.image = self._create_image()
        self.image1 = self._create_image()
        self.image2 = self._create_image()
        self.image3 = self._create_image()
        self.image4 = self._create_image()
        self.image5 = self._create_image()
        self.api_authentication(user=self.user)
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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.profile1.id, "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.profile1.id, "paper": None, "group": "2"},
                {"profile": self.expert_profile.profile.id, "paper": None, "group": "3"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
            "verifying_explanation": {
                "accessibility": True,
                "acquisition_tax": None,
                "actual_building_category": "단독주택",
                "actual_expenses": 50000,
                "actual_land_category": 7,
                "address": address_vars,
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
                "heating_type": 1,
                "heating_type_info": "",
                "high_school": "전남대사범대학부설고등",
                "high_school_by_foot": True,
                "high_school_required_time": 10,
                "insurance": self.expert_profile.insurances.first().id,
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
                "ledger_building_category": "단독주택",
                "legal_status": True,
                "local_education_tax": None,
                "management": 2,
                "matters_of_violation": "",
                "medical_center": "전남대병원",
                "medical_center_by_foot": False,
                "medical_center_required_time": 20,
                "middle_school": "전대사범대학부설중",
                "middle_school_by_foot": True,
                "middle_school_required_time": 10,
                "net_area": 50,
                "noise_status": 1,
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
                "rental_housing_registration": 2,
                "requesting_condition_info": "",
                "seismic_capacity": "해당사항없음",
                "seismic_design": "해당사항없음",
                "special_tax": None,
                "speculative_area": None,
                "subway_by_foot": False,
                "subway_required_time": 10,
                "subway_station": "상무",
                "sunshine_status": 1,
                "sunshine_status_info": "",
                "undesirable_facilities": False,
                "undesirable_facilities_info": "",
                "unit_planning_area_others": "",
                "use_area": "",
                "use_district": "",
                "use_zone": "",
                "vibration": 1,
                "wall_crack_status": False,
                "wall_crack_status_info": "",
                "wall_paper_status": 1,
                "wall_paper_status_info": "",
                "water_capacity_status": True,
                "water_capacity_status_info": "",
                "water_damage_status": False,
                "water_damage_status_info": "",
                "water_leak_status": False,
                "water_leak_status_info": "",
                "year_of_completion": 1995,
            },
        }
        self.paper_with_verifying_explanation = self.client.post(
            self.list_url, data=data, format="json"
        ).data
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
            "contractor": self.paper_with_verifying_explanation["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse(
                "create-explanation-signature",
                kwargs={"id": self.paper_with_verifying_explanation["id"]},
            ),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_explanation_signature_create_unauthorization(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        data = {
            "contractor": self.paper_with_verifying_explanation["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse(
                "create-explanation-signature",
                kwargs={"id": self.paper_with_verifying_explanation["id"]},
            ),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_explanation_signature_create_with_paper_done(self):
        data = {
            "contractor": self.paper_with_verifying_explanation["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse(
                "create-signature", kwargs={"id": self.paper_with_verifying_explanation["id"]}
            ),
            data,
        )
        response = self.client.post(
            reverse(
                "create-explanation-signature",
                kwargs={"id": self.paper_with_verifying_explanation["id"]},
            ),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=self.profile1.user)
        data = {
            "contractor": self.paper_with_verifying_explanation["paper_contractors"][1]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse(
                "create-signature", kwargs={"id": self.paper_with_verifying_explanation["id"]}
            ),
            data,
        )
        response = self.client.post(
            reverse(
                "create-explanation-signature",
                kwargs={"id": self.paper_with_verifying_explanation["id"]},
            ),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=self.expert_profile.profile.user)
        data = {
            "contractor": self.paper_with_verifying_explanation["paper_contractors"][2]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse(
                "create-signature", kwargs={"id": self.paper_with_verifying_explanation["id"]}
            ),
            data,
        )
        response = self.client.post(
            reverse(
                "create-explanation-signature",
                kwargs={"id": self.paper_with_verifying_explanation["id"]},
            ),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            reverse("papers-detail", kwargs={"pk": self.paper_with_verifying_explanation["id"]})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], PaperStatus.DONE)

    def test_explanation_signature_create_after_paper_done(self):
        data = {
            "contractor": self.paper["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        paper = Paper.objects.get(id=2)
        paper_status = paper.status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        response = self.client.post(
            reverse(
                "create-explanation-signature",
                kwargs={"id": self.paper_with_verifying_explanation["id"]},
            ),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("완료 또는 거절된 계약서는 서명을 추가할 수 없습니다."))

    def test_explanation_signature_create_duplications(self):
        data = {
            "contractor": self.paper_with_verifying_explanation["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        self.client.post(
            reverse("create-explanation-signature", kwargs={"id": self.paper["id"]}), data
        )
        response = self.client.post(
            reverse(
                "create-explanation-signature",
                kwargs={"id": self.paper_with_verifying_explanation["id"]},
            ),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("이미 서명이 등록되어있습니다."))

    def test_explanation_signature_update(self):
        data = {
            "contractor": self.paper_with_verifying_explanation["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse(
                "create-explanation-signature",
                kwargs={"id": self.paper_with_verifying_explanation["id"]},
            ),
            data,
        )

        data = {
            "contractor": self.paper_with_verifying_explanation["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.put(
            reverse(
                "update-explanation-signature",
                kwargs={
                    "paper_id": self.paper_with_verifying_explanation["id"],
                    "pk": response.data["id"],
                },
            ),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_explanation_signature_update_after_paper_done(self):
        data = {
            "contractor": self.paper_with_verifying_explanation["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse(
                "create-explanation-signature",
                kwargs={"id": self.paper_with_verifying_explanation["id"]},
            ),
            data,
        )
        paper = Paper.objects.get(id=2)
        paper_status = paper.status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        data = {
            "contractor": self.paper_with_verifying_explanation["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.put(
            reverse(
                "update-explanation-signature",
                kwargs={"paper_id": paper.id, "pk": response.data["id"]},
            ),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("완료 또는 거절된 계약서는 서명을 수정할 수 없습니다."))

    def test_signature_create(self):
        data = {
            "contractor": self.paper["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse("create-signature", kwargs={"id": self.paper["id"]}), data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signature_create_unauthorization(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        data = {
            "contractor": self.paper["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse("create-signature", kwargs={"id": self.paper["id"]}), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_signature_create_with_paper_done(self):
        data = {
            "contractor": self.paper["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse("create-signature", kwargs={"id": self.paper["id"]}), data
        )
        self.client.force_authenticate(user=self.profile1.user)
        data = {
            "contractor": self.paper["paper_contractors"][1]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse("create-signature", kwargs={"id": self.paper["id"]}), data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse("papers-detail", kwargs={"pk": self.paper["id"]}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], PaperStatus.DONE)

    def test_signature_create_after_paper_done(self):
        data = {
            "contractor": self.paper["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        paper = Paper.objects.get(id=1)
        paper_status = paper.status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        response = self.client.post(
            reverse("create-signature", kwargs={"id": self.paper["id"]}), data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("완료 또는 거절된 계약서는 서명을 추가할 수 없습니다."))

    def test_signature_create_duplications(self):
        data = {
            "contractor": self.paper["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        self.client.post(reverse("create-signature", kwargs={"id": self.paper["id"]}), data)
        response = self.client.post(
            reverse("create-signature", kwargs={"id": self.paper["id"]}), data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("이미 서명이 등록되어있습니다."))

    def test_signature_update(self):
        data = {
            "contractor": self.paper["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse("create-signature", kwargs={"id": self.paper["id"]}), data
        )

        data = {
            "contractor": self.paper["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.put(
            reverse(
                "update-signature",
                kwargs={"paper_id": self.paper["id"], "pk": response.data["id"]},
            ),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signature_update_after_paper_done(self):
        data = {
            "contractor": self.paper["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse("create-signature", kwargs={"id": self.paper["id"]}), data
        )
        paper = Paper.objects.get(id=1)
        paper_status = paper.status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        data = {
            "contractor": self.paper["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.put(
            reverse("update-signature", kwargs={"paper_id": paper.id, "pk": response.data["id"]}),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("완료 또는 거절된 계약서는 서명을 수정할 수 없습니다."))

    def test_paper_update_and_delete_after_24H_from_first_signature(self):
        data = {
            "contractor": self.paper["paper_contractors"][0]["id"],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.post(
            reverse("create-signature", kwargs={"id": self.paper["id"]}), data
        )
        paper = Paper.objects.filter(id=1)
        new_updated_at = timezone.now() - timedelta(hours=24, minutes=2)
        paper.update(updated_at=new_updated_at)
        signature = Signature.objects.filter(id=1)
        new_updated_at = timezone.now() - timedelta(hours=24, minutes=1)
        signature.update(updated_at=new_updated_at)

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
            "options": [1, 2, 3],
            "paper_contractors": [
                {"profile": self.profile.id, "paper": None, "group": "1"},
                {"profile": self.profile1.id, "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트1",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.put(
            reverse("papers-detail", kwargs={"pk": self.paper["id"]}), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("최초 서명 후 24시간이 지나면 계약서를 수정 할 수 없습니다."))

        response = self.client.delete(
            reverse("papers-detail", kwargs={"pk": self.paper["id"]}), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("최초 서명 후 24시간이 지나면 계약서를 삭제 할 수 없습니다."))
