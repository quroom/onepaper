from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from addresses.models import Address
from profiles.models import CustomUser, Profile, ExpertProfile

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
        sigunguCd = '29170', bjdongCd = '29170', platGbCd = '', bun = '973', ji = '17', dong = '202', ho='307')
        self.profile = Profile.objects.create(user=self.user, address=address, bank_name="광주은행", account_number="120982711", mobile_number="010-1234-5678")
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

    def create_user_profile(index=0, is_expert=False):
        user = CustomUser.objects.create_user(username="test"+str(index), email="test@naver.com", password="some_strong_password",
                                              bio="bio", name="김주영", birthday="1955-02-12")
        address = Address.objects.create(old_address='광주 광산구 명도동 169', new_address='광주광역시 광산구 가마길 2-21', 
        sigunguCd = '29170', bjdongCd = '29170', platGbCd = '', bun = '973', ji = '17', dong = '202', ho='307')
        profile = Profile.objects.create(user=user, address=address, bank_name="국민은행", account_number="98373737372", mobile_number="010-9827-111"+str(index))
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