import json
import tempfile
import random
import os

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.test import override_settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory
from urllib.request import urlopen

from profiles.serializers import ProfileSerializer
from addresses.models import Address
from profiles.models import CustomUser, Profile, ExpertProfile

class AllowedUserTestCase(APITestCase):
    detail_url = reverse("allowed-user-detail", args=(1,))
    list_url = reverse("profiles-list")

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test",
                                                   email="test@naver.com",
                                                   password="some_strong_password",
                                                   bio="bio",
                                                   name="김주영",
                                                   birthday="1955-02-12")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def create_user(self, id):
        self.user = CustomUser.objects.create_user(username="test"+str(id),
                                                   email="test@naver.com",
                                                   password="some_strong_password",
                                                   bio="bio",
                                                   name="김주영"+str(id),
                                                   birthday="1955-02-12")

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

    def test_allowed_user_create(self):
        # print(reverse("allowed-user-detail", args=(1,)))
        self.create_profile()
        self.create_user(1)
        self.create_user(2)

        self.client.post(reverse(
            "allowed-user-detail", args=(1,)), {"allowed_users": {"username":"test", "name":"김주영"}}, format="json")
        self.client.post(reverse(
            "allowed-user-detail", args=(1,)), {"allowed_users": {"username":"test1", "name":"김주영1"}}, format="json")
        response = self.client.post(reverse(
            "allowed-user-detail", args=(1,)), {"allowed_users": {"username":"test2", "name":"김주영2"}}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

MEDIA_ROOT = tempfile.mkdtemp()
@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ExpertProfileTestCase(APITestCase):
    list_url = reverse("profiles-list")

    def _create_image(self):
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')

        return open(f.name, mode='rb')

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def setUp(self):
        self.image = self._create_image()
        self.image1 = self._create_image()
        self.image2 = self._create_image()
        self.image3 = self._create_image()
        self.user = CustomUser.objects.create_user(username="test",
                                                   email="test@naver.com",
                                                   password="some_strong_password",
                                                   bio="bio",
                                                   name="김주영",
                                                   birthday="1955-02-12",
                                                   is_expert=True)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def tearDown(self):
        self.image.close()
        os.remove(self.image.name)
        self.image1.close()
        os.remove(self.image1.name)
        self.image2.close()
        os.remove(self.image2.name)
        self.image3.close()
        os.remove(self.image3.name)

    def test_customuser(self):
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "test")
        self.assertEqual(response.data["email"], "test@naver.com")
        self.assertEqual(response.data["bio"], "bio")
        self.assertEqual(response.data["name"], "김주영")
        self.assertEqual(response.data["birthday"], "1955-02-12")
        self.assertEqual(response.data["is_expert"], True)

    def create_user_expert_profile(self, index=0, is_expert=False):
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
       
    def create_expert_profile(self):
        #FIXME: Need to create objects with model directely
        data = {
            "mobile_number": "010-1234-1234",
            "bank_name": "국민은행",
            "account_number": "94334292963",
            "address.old_address": '광주 광산구 명도동 169',
            "address.new_address": '광주광역시 광산구 가마길 2-21',
            "address.sigunguCd": '29170',
            "address.bjdongCd": '29170',
            "address.platGbCd": '',
            "address.bun":'973',
            "address.ji":'17',
            "address.dong":'',
            "address.ho":'2층',
            "expert_profile.registration_number": "2020118181-11",
            "expert_profile.shop_name": "광주부동산중개",
            "expert_profile.registration_certificate": self.image,
            "expert_profile.agency_license": self.image1,
            "expert_profile.stamp": self.image2,
            "expert_profile.garantee_insurance": self.image3
        }
        response = self.client.post(self.list_url, data=data)
        return response

    def test_expert_profile_create(self):
        response = self.create_expert_profile()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["mobile_number"], "010-1234-1234")
        self.assertEqual(response.data["bank_name"], "국민은행")
        self.assertEqual(response.data["account_number"], "94334292963")
        self.assertEqual(response.data["address"]["old_address"],  '광주 광산구 명도동 169')
        self.assertEqual(response.data["address"]["dong"], '')
        self.assertEqual(response.data["address"]["ho"], '2층')
        self.assertEqual(
            response.data["expert_profile"]["registration_number"], "2020118181-11")
        self.assertEqual(
            response.data["expert_profile"]["shop_name"], "광주부동산중개")
        self.assertEqual(
            response.data["expert_profile"]["status"], 0)
        #FIXME: Need to add image test code

    def test_expert_profile_update(self):
        self.create_expert_profile()
        data = {
            "mobile_number": "010-4334-2929",
            "address.ho": "1층",
            "bank_name": "국민은행_",
            "account_number": "94334292963_",
            "expert_profile.registration_number": "2020118181-11_",
            "expert_profile.shop_name": "광주부동산중개_",
        }
        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["mobile_number"], "010-4334-2929")
        self.assertEqual(response.data["address"]["ho"], "1층")
        self.assertEqual(response.data["bank_name"], "국민은행_")
        self.assertEqual(response.data["account_number"], "94334292963_")
        self.assertEqual(
            response.data["expert_profile"]["registration_number"], "2020118181-11_")
        self.assertEqual(
            response.data["expert_profile"]["shop_name"], "광주부동산중개_")

    def test_profile_update_by_random_user(self):
        random_user = CustomUser.objects.create_user(
            username="random", password="psw123123123")
        self.create_expert_profile()
        self.client.force_authenticate(user=None)
        response = self.client.put(reverse("profiles-detail", kwargs={"pk": 1}),
                                   {"bank_name": "hacked!!!"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expert_profile_delete(self):
        self.create_expert_profile()
        response = self.client.delete(
            reverse("profiles-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_approve_expert(self):
        expert_profile = self.create_user_expert_profile(is_expert=True)
        self.assertEqual(expert_profile.status, 0)
        expert_profile2 = self.create_user_expert_profile(is_expert=True, index=1)
        self.superuser = CustomUser.objects.create_superuser("admin", "admin@naver.com", '1234')
        self.token = Token.objects.create(user=self.superuser)
        self.api_authentication()
        response = self.client.put("/api/approve-experts/", data={"profiles":[1]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['status'], 1)
        self.assertEqual(response.data['results'][1]['status'], 0)
        response = self.client.delete("/api/approve-experts/", data={"profiles":[1]}, format="json")
        self.assertEqual(response.data['results'][0]['status'], 2)
        self.assertEqual(response.data['results'][1]['status'], 0)
        response = self.client.put("/api/approve-experts/", data={"profiles":[1,2]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['status'], 1)
        self.assertEqual(response.data['results'][1]['status'], 1)
        response = self.client.delete("/api/approve-experts/", data={"profiles":[1,2]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['status'], 2)
        self.assertEqual(response.data['results'][1]['status'], 2)

    def test_approve_expert_with_no_profiles(self):
        expert_profile = self.create_user_expert_profile(is_expert=True)
        self.assertEqual(expert_profile.status, 0)
        expert_profile2 = self.create_user_expert_profile(is_expert=True, index=1)
        self.superuser = CustomUser.objects.create_superuser("admin", "admin@naver.com", '1234')
        self.token = Token.objects.create(user=self.superuser)
        self.api_authentication()
        response = self.client.put("/api/approve-experts/", data={"profiles":[]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("전문가가 선택되지 않았습니다."))
        response = self.client.put("/api/approve-experts/", data={"profiles":[3]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("승인 가능한 전문가가 선택되지 않았습니다."))
        response = self.client.delete("/api/approve-experts/", data={"profiles":[5]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("전문가가 선택되지 않았습니다."))

class ProfileTestCase(APITestCase):

    list_url = reverse("profiles-list")
    paper_list = reverse("papers-list")
    mandate_list = reverse("mandates-list")

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", email="test@naver.com", password="some_strong_password",
                                                   bio="bio", name="김주영", birthday="1955-02-12")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

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

    def create_expert_profile(self):
        #FIXME: Need to create objects with model directely
        data = {
            "mobile_number": "010-1234-1234",
            "bank_name": "국민은행",
            "account_number": "94334292963",
            "address.old_address": '광주 광산구 명도동 169',
            "address.new_address": '광주광역시 광산구 가마길 2-21',
            "address.sigunguCd": '29170',
            "address.bjdongCd": '29170',
            "address.platGbCd": '',
            "address.bun":'973',
            "address.ji":'17',
            "address.dong":'',
            "address.ho":'2층',
            "expert_profile.registration_number": "2020118181-11",
            "expert_profile.shop_name": "광주부동산중개",
            "expert_profile.registration_certificate": self.image,
            "expert_profile.agency_license": self.image1,
            "expert_profile.stamp": self.image2,
            "expert_profile.garantee_insurance": self.image3
        }
        response = self.client.post(self.list_url, data=data)
        return response

    def test_profile_create(self):
        response = self.create_profile()
    
    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_retrieve(self):
        self.create_profile()
        response = self.client.get(reverse("profiles-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], "test")

    def test_profile_update_by_owner(self):
        self.create_profile()
        data = {
            "mobile_number": "010-4334-2929",
            "address.ho":'1층',
            "bank_name": "우리은행",
            "account_number": "938271122121"
        }
        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["mobile_number"], "010-4334-2929")
        self.assertEqual(response.data["address"]["ho"], "1층")
        self.assertEqual(response.data["bank_name"], "우리은행")
        self.assertEqual(response.data["account_number"], "938271122121")

    def test_profile_update_by_random_user(self):
        random_user = CustomUser.objects.create_user(
            username="random", password="psw123123123")
        self.create_profile()
        self.client.force_authenticate(user=None)
        response = self.client.put(reverse("profiles-detail", kwargs={"pk": 1}),
                                   {"bank_name": "hacked!!!"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_delete(self):
        self.create_profile()
        response = self.client.delete(
            reverse("profiles-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_profile_delete_with_paper(self):
        response = self.create_profile()
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
                {"profile": response.data["id"], "paper": None, "group": "0"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.paper_list, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(
            reverse("profiles-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_with_paper(self):
        response = self.create_profile()
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
                {"profile": response.data["id"], "paper": None, "group": "0"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "to_date": "2020-11-30",
            "trade_category": 1,
        }
        response = self.client.post(self.paper_list, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": 1}),
            data={
                "mobile_number": "010-1234-5678"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_with_mandate(self):
        response = self.create_profile()
        user = CustomUser.objects.create_user(username="test"+str(id),
                                                   email="test@naver.com",
                                                   password="some_strong_password",
                                                   bio="bio",
                                                   name="김주영"+str(id),
                                                   birthday="1955-02-12")
        self.token = Token.objects.create(user=user)
        self.api_authentication()
        response2 = self.create_profile()
        data = {
            "designator": response2.data["id"],
            "designee": response.data["id"],
            "content": "제1조 상기 위임인은 수임인에게 부동산 기본정보에 기재된 거래 대상 부동산의 계약에 관한 사무를 위임한다.<br>제2조 상기 위임인은 거래계약체결 상대방에게 위임사실을 알리기 위하여 위임장 사본을 제공한다.",
            "from_date": "2020-12-01",
            "to_date": "2020-12-31",
            "address.old_address": "서울 강동구 성내동 111-39",
            "address.new_address": "서울 강동구 풍성로 87-14",
            "address.sigunguCd": "11740",
            "address.bjdongCd": "11740",
            "address.bun": "111",
            "address.ji": "39"
        }
        response = self.client.post(self.mandate_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": 2}),
            data={
                "mobile_number": "010-1234-5678"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_delete_with_mandate(self):
        response = self.create_profile()
        user = CustomUser.objects.create_user(username="test"+str(id),
                                                   email="test@naver.com",
                                                   password="some_strong_password",
                                                   bio="bio",
                                                   name="김주영"+str(id),
                                                   birthday="1955-02-12")
        self.token = Token.objects.create(user=user)
        self.api_authentication()
        response2 = self.create_profile()
        data = {
            "designator": response2.data["id"],
            "designee": response.data["id"],
            "content": "제1조 상기 위임인은 수임인에게 부동산 기본정보에 기재된 거래 대상 부동산의 계약에 관한 사무를 위임한다.<br>제2조 상기 위임인은 거래계약체결 상대방에게 위임사실을 알리기 위하여 위임장 사본을 제공한다.",
            "from_date": "2020-12-01",
            "to_date": "2020-12-31",
            "address.old_address": "서울 강동구 성내동 111-39",
            "address.new_address": "서울 강동구 풍성로 87-14",
            "address.sigunguCd": "11740",
            "address.bjdongCd": "11740",
            "address.bun": "111",
            "address.ji": "39"
        }
        response = self.client.post(self.mandate_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(
            reverse("profiles-detail", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_default_profile(self):
        response = self.create_profile()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["is_default"], True)
        response2 = self.create_profile()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["is_default"], True)
        self.assertEqual(Profile.objects.filter(is_default=False).count(), 1)

        response = self.client.post(reverse("default-profile", kwargs={"pk": response.data["id"]}))
        self.assertEqual(response.data["is_default"], True)

class CustomUserTestCase(APITestCase):
    profiles_list_url = reverse("profiles-list")
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", email="test@naver.com", password="some_strong_password",
                                                   bio="bio", name="김주영", birthday="1955-02-12")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

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
        response = self.client.post(self.profiles_list_url, data=data)
        return response

    def test_user_registration(self):
        data = {"username": "testcase", "email": "testcase@naver.com",
                "password1": "some_strong_password", "password2": "some_strong_password",
                "bio": "test", "name": "김주영", "birthday": "1955-02-12", "is_expert": False}
        response = self.client.post("/api/dj-rest-auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customuser(self):
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "test")
        self.assertEqual(response.data["email"], "test@naver.com")
        self.assertEqual(response.data["bio"], "bio")
        self.assertEqual(response.data["name"], "김주영")
        self.assertEqual(response.data["birthday"], "1955-02-12")
        self.assertEqual(response.data["is_expert"], False)

    def test_user_update_by_owner(self):
        data = {
            "birthday": "1955-01-01"
        }
        response = self.client.put(
            reverse("user-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["birthday"], "1955-01-01")

    def test_user_update_with_profile(self):
        self.create_profile()
        data = {
            "birthday": "1955-01-01"
        }
        response = self.client.put(
            reverse("user-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("프로필이 존재하는 경우 회원 정보를 수정할 수 없습니다."))

    def test_user_delete(self):
        data = {
            "username": "test",
            "name": "김주영",
            "email": "test@naver.com"
        }
        response = self.client.delete(
            reverse("user-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_delete_with_profile(self):
        self.create_profile()
        data = {
            "username": "test",
            "name": "김주영",
            "email": "test@naver.com"
        }
        response = self.client.delete(
            reverse("user-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_delete_key_error(self):
        data = {
            "username": "test",
            "email": "test@naver.com"
        }
        response = self.client.delete(
            reverse("user-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_delete_unmatched(self):
        data = {
            "username": "test",
            "name": "김주영11",
            "email": "test@naver.com"
        }
        response = self.client.delete(
            reverse("user-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)