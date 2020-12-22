import datetime
import tempfile
import os

from PIL import Image
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from addresses.models import Address
from profiles.models import AllowedUser, CustomUser, Profile, ExpertProfile
from papers.models import Paper, PaperStatus

# Create your tests here.
class PaperTestCase(APITestCase):
    list_url = reverse("papers-list")
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
        address = Address.objects.create(old_address='광주 광산구 명도동 169', new_address='광주광역시 광산구 가마길 2-21',
                                         sigunguCd='29170', bjdongCd='29170', platGbCd='', bun='973', ji='17', dong='202', ho='307')
        self.profile = Profile.objects.create(user=self.user, address=address, bank_name="광주은행",
        account_number="120982711", mobile_number="010-1234-5678")
        self.api_authentication(self.user)
        self.create_profile()

    def create_profile(self):
        data = {
            "mobile_number": "010-1234-1234",
            "address.old_address": '광주 광산구 명도동 169',
            "address.new_address": '광주광역시 광산구 가마길 2-21',
            "address.sigunguCd": '29170',
            "address.bjdongCd": '29170',
            "address.platGbCd": '',
            "address.bun":'973',
            "address.ji":'17',
            "address.dong":'',
            "address.ho":'2층',
            "bank_name": "국민은행",
            "account_number": "94334292963"
        }
        response = self.client.post(self.list_url, data=data)
        return response

    def create_user_profile(self, id=0, is_expert=False):
        user = CustomUser.objects.create_user(username="test"+str(id), email="test@naver.com", password="some_strong_password",
                                              bio="bio", name="김주영", birthday="1955-02-12")
        address = Address.objects.create(old_address='광주 광산구 명도동 169', new_address='광주광역시 광산구 가마길 2-21', 
        sigunguCd = '29170', bjdongCd = '29170', platGbCd = '', bun = '973', ji = '17', dong = '202', ho='307')
        profile = Profile.objects.create(user=user, address=address, bank_name="국민은행", account_number="98373737372", mobile_number="010-9827-111"+str(id))
        AllowedUser.objects.create(profile=profile)
        if is_expert:
            expert_profile = ExpertProfile.objects.create(
                profile=profile, registration_number="2020118181-11", shop_name="효암중개사")
            return expert_profile
        return profile

    def test_paper_create(self):
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_paper_create_without_self(self):
        profile2 = self.create_user_profile(id=2)
        profile2_allowed_user = AllowedUser.objects.get(profile=profile2)
        profile2_allowed_user.allowed_users.add(self.user)
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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

    def test_paper_create_with_contractors(self):
        expert_profile = self.create_user_profile(id=1, is_expert=True)
        expert_profile.status = ExpertProfile.APPROVED
        expert_profile.save()
        expert_profile_allowed_user = AllowedUser.objects.get(profile=expert_profile.profile)
        expert_profile_allowed_user.allowed_users.add(self.user)
        profile2 = self.create_user_profile(id=2)
        profile2_allowed_user = AllowedUser.objects.get(profile=profile2)
        profile2_allowed_user.allowed_users.add(self.user)
        
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_paper_create_with_same_profiles(self):
        profile2 = self.create_profile()
        
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
                {"profile": 1, "paper": None, "group": "0"},
                {"profile": 2, "paper": None, "group": "1"}
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_paper_create_with_contractors_unallowed(self):
        expert_profile = self.create_user_profile(id=1, is_expert=True)
        profile2 = self.create_user_profile(id=2)
        
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
                {"profile": expert_profile.id, "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_paper_create_with_expert_as_trader(self):
        expert_profile = self.create_user_profile(id=1, is_expert=True)
        expert_profile.status = ExpertProfile.APPROVED
        expert_profile.save()
        expert_profile_allowed_user = AllowedUser.objects.get(profile=expert_profile.profile)
        expert_profile_allowed_user.allowed_users.add(self.user)
        profile2 = self.create_user_profile(id=2)
        profile2_allowed_user = AllowedUser.objects.get(profile=profile2)
        profile2_allowed_user.allowed_users.add(self.user)
        
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
                {"profile": expert_profile.profile.id, "paper": None, "group": "1"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_paper_create_with_unapproved_expert(self):
        expert_profile = self.create_user_profile(id=1, is_expert=True)
        expert_profile_allowed_user = AllowedUser.objects.get(profile=expert_profile.profile)
        expert_profile_allowed_user.allowed_users.add(self.user)
        profile2 = self.create_user_profile(id=2)
        profile2_allowed_user = AllowedUser.objects.get(profile=profile2)
        profile2_allowed_user.allowed_users.add(self.user)
        
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
    
    def test_paper_create_with_expert_without_verifying_explnation(self):
        expert_profile = self.create_user_profile(id=1, is_expert=True)
        expert_profile_allowed_user = AllowedUser.objects.get(profile=expert_profile.profile)
        expert_profile_allowed_user.allowed_users.add(self.user)
        self.api_authentication(user=expert_profile.profile.user)
        
        profile2 = self.create_user_profile(id=2)
        profile2_allowed_user = AllowedUser.objects.get(profile=profile2)
        profile2_allowed_user.allowed_users.add(self.user)
        
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
    
    def test_paper_create_with_expert_without_expert(self):
        expert_profile = self.create_user_profile(id=1, is_expert=True)
        expert_profile_allowed_user = AllowedUser.objects.get(profile=expert_profile.profile)
        expert_profile_allowed_user.allowed_users.add(self.user)
        self.api_authentication(user=expert_profile.profile.user)
        
        profile2 = self.create_user_profile(id=2)
        profile2_allowed_user = AllowedUser.objects.get(profile=profile2)
        profile2_allowed_user.allowed_users.add(self.user)
        
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
                {"profile": profile2.id, "paper": None, "group": "1"}
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_paper_update(self):
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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

    def test_paper_delete(self):
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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
        self.user = CustomUser.objects.create_user(username="test",
                                                    email="test@naver.com",
                                                    password="some_strong_password",
                                                    bio="bio",
                                                    name="김주영",
                                                    birthday="1955-02-12")
        self.api_authentication(user=self.user)
        address = Address.objects.create(old_address="광주 광산구 명도동 169", new_address="광주광역시 광산구 가마길 2-21",
                                         sigunguCd="29170", bjdongCd="29170", platGbCd="", bun="973", ji="17", dong="202", ho="307")
        self.profile = Profile.objects.create(user=self.user, address=address, bank_name="국민은행", account_number="1908281111", mobile_number="010-3982-1111")
        user = CustomUser.objects.create_user(username="test1",
                                                    email="test1@naver.com",
                                                    password="some_strong_password",
                                                    bio="bio",
                                                    name="김길동",
                                                    birthday="1955-02-12")
        address = Address.objects.create(old_address="서울특별시 강남구 명도동 222", new_address="서울특별시 강남구 강남대로 2-21",
                                         sigunguCd="29170", bjdongCd="29170", platGbCd="", bun="973", ji="17", dong="202", ho="307")
        self.profile1 = Profile.objects.create(user=user, address=address, bank_name="서울은행", account_number="1111111", mobile_number="010-3982-2222")
        profile1_allowed_user = AllowedUser.objects.create(profile=self.profile1)
        profile1_allowed_user.allowed_users.add(self.user)

        user = CustomUser.objects.create_user(username="expert",
                                                    email="expert@naver.com",
                                                    password="some_strong_password",
                                                    bio="bio",
                                                    name="서주은",
                                                    birthday="1955-02-12")
        address = Address.objects.create(old_address="세종시 빛가람동 222", new_address="세종시 빛가람로 2-21",
                                         sigunguCd="29170", bjdongCd="29170", platGbCd="", bun="973", ji="17", dong="202", ho="307")
        profile2 = Profile.objects.create(user=user, address=address, bank_name="충북은행", account_number="1111111", mobile_number="010-3982-5555")
        self.expert_profile = ExpertProfile.objects.create(profile=profile2, registration_number="2020118181-11", shop_name="효암중개사")

        address = Address.objects.create(old_address="세종시 빛가람동 222", new_address="세종시 빛가람로 2-21",
                                         sigunguCd="29170", bjdongCd="29170", platGbCd="", bun="973", ji="17", dong="202", ho="307")
        data = {
            "address": {
                "ho": "22",
                "old_address": "광주 광산구 명도동 169",
                "dong": "111"
            },
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

    def test_signature_create(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': self.image
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signature_create_unauthentication(self):
        self.client.force_authenticate(user=self.expert_profile.profile.user)
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': self.image
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_signature_create_with_paper_done(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': self.image
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.api_authentication(user=self.profile1.user)
        data = {
            'contractor': self.paper['paper_contractors'][1]['id'],
            'image': self.image1
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('papers-detail', kwargs={'pk':self.paper['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], PaperStatus.DONE)

    def test_signature_create_error_with_done_paper(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': self.image
        }
        paper = Paper.objects.get(id=1)
        paper_status = paper.status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signature_create_duplications(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': self.image
        }
        self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signature_update(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': self.image
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)

        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': self.image1
        }
        response = self.client.put(reverse('update-signature', kwargs={'paper_id':self.paper['id'], 'pk':response.data['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signature_update_with_done_paper(self):
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': self.image
        }
        response = self.client.post(reverse('create-signature', kwargs={'id':self.paper['id']}), data)
        paper = Paper.objects.get(id=1)
        paper_status = paper.status
        paper_status.status = PaperStatus.DONE
        paper_status.save()
        data = {
            'contractor': self.paper['paper_contractors'][0]['id'],
            'image': self.image1
        }
        response = self.client.put(reverse('update-signature', kwargs={'paper_id':paper.id, 'pk':response.data['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)