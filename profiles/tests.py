import json
import tempfile
import random

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.urls import reverse
from django.test import override_settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory
from urllib.request import urlopen

from profiles.serializers import ProfileSerializer
from profiles.models import CustomUser, Profile, ExpertProfile


class RegistrationTestCase(APITestCase):

    def test_normal_user_registration(self):
        data = {"username": "testcase", "email": "test@naver.com",
                "password1": "some_strong_password", "password2": "some_strong_password",
                "bio": "test", "name": "김상은", "birthday": "1988-05-12", "request_expert": False}
        response = self.client.post("/api/rest-auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileTestCase(APITestCase):

    list_url = reverse("profile-list")

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", email="test@naver.com", password="some_strong_password",
                                                   bio="bio", name="김상은", birthday="1988-05-12")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_customuser(self):
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "test")
        self.assertEqual(response.data["email"], "test@naver.com")
        self.assertEqual(response.data["bio"], "bio")
        self.assertEqual(response.data["name"], "김상은")
        self.assertEqual(response.data["birthday"], "1988-05-12")

    def create_profile(self):
        profile = Profile.objects.create(user=self.user,
                                         profile_name="기본프로필",
                                         mobile_number="010-7777-1618",
                                         address="광주광역시 남구 서문대로 690번길 3",
                                         bank_name="국민은행",
                                         account_number="94334292963")
        return profile

    def create_expert_profile(self):
        data = {
            "profile_name": "기본프로필",
            "mobile_number": "010-7777-1618",
            "address": "광주광역시 남구 서문대로 690번길 3",
            "bank_name": "국민은행",
            "account_number": "94334292963"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["profile_name"], "기본프로필")
        self.assertEqual(response.data["mobile_number"], "010-7777-1618")
        self.assertEqual(response.data["address"], "광주광역시 남구 서문대로 690번길 3")
        self.assertEqual(response.data["bank_name"], "국민은행")
        self.assertEqual(response.data["account_number"], "94334292963")

    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_retrieve(self):
        self.create_profile()
        response = self.client.get(reverse("profile-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], "test")

    def test_profile_updated_by_owner(self):
        self.create_profile()
        data = {
            "profile_name": "기본프로필1",
            "mobile_number": "010-4334-2929",
            "address": "광주광역시 북구 중흥동",
            "bank_name": "우리은행",
            "account_number": "938271122121"
        }
        response = self.client.put(
            reverse("profile-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile_name"], "기본프로필1")
        self.assertEqual(response.data["mobile_number"], "010-4334-2929")
        self.assertEqual(response.data["address"], "광주광역시 북구 중흥동")
        self.assertEqual(response.data["bank_name"], "우리은행")
        self.assertEqual(response.data["account_number"], "938271122121")

    def test_profile_updated_by_random_user(self):
        random_user = CustomUser.objects.create_user(
            username="random", password="psw123123123")
        self.create_profile()
        self.client.force_authenticate(user=None)
        response = self.client.put(reverse("profile-detail", kwargs={"pk": 1}),
                                   {"profile_name": "hacked!!!"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_delete(self):
        self.create_profile()
        response = self.client.delete(
            reverse("profile-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ExpertProfileTestCase(APITestCase):
    list_url = reverse("profile-list")

    def _create_image(self):
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')

        return open(f.name, mode='rb')

    def setUp(self):
        self.image = self._create_image()
        self.image1 = self._create_image()
        self.image2 = self._create_image()
        self.user = CustomUser.objects.create_user(username="test",
                                                   email="test@naver.com",
                                                   password="some_strong_password",
                                                   bio="bio",
                                                   name="김상은",
                                                   birthday="1988-05-12",
                                                   request_expert=True)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def tearDown(self):
        self.image.close()
        os.remove(self.image.name)
        self.image1.close()
        os.remove(self.image1.name)
        self.image2.close()
        os.remove(self.image2.name)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_customuser(self):
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "test")
        self.assertEqual(response.data["email"], "test@naver.com")
        self.assertEqual(response.data["bio"], "bio")
        self.assertEqual(response.data["name"], "김상은")
        self.assertEqual(response.data["birthday"], "1988-05-12")
        self.assertEqual(response.data["request_expert"], True)

    def create_expert_profile(self):
        # FIXME: Need to create objects with model directely
        data = {
            "profile_name": "기본프로필",
            "mobile_number": "010-7777-1618",
            "address": "광주광역시 남구 서문대로 690번길 3",
            "bank_name": "국민은행",
            "account_number": "94334292963",
            "expert_profile.registration_number": "2020118181-11",
            "expert_profile.shop_name": "광주부동산중개",
            "expert_profile.business_registration_certificate": self.image,
            "expert_profile.agency_license": self.image1,
            "expert_profile.stamp": self.image2
        }
        response = self.client.post(self.list_url, data=data)
        return response

    def test_expert_profile_create(self):
        response = self.create_expert_profile()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["profile_name"], "기본프로필")
        self.assertEqual(response.data["mobile_number"], "010-7777-1618")
        self.assertEqual(response.data["address"], "광주광역시 남구 서문대로 690번길 3")
        self.assertEqual(response.data["bank_name"], "국민은행")
        self.assertEqual(response.data["account_number"], "94334292963")
        self.assertEqual(
            response.data["expert_profile"]["registration_number"], "2020118181-11")
        self.assertEqual(
            response.data["expert_profile"]["shop_name"], "광주부동산중개")
        # FIXME: Need to add image test code

    def test_expert_profile_update(self):
        self.create_expert_profile()
        data = {
            "profile_name": "기본프로필_",
            "mobile_number": "010-4334-2929",
            "address": "광주광역시 남구 서문대로 690번길 3_",
            "bank_name": "국민은행_",
            "account_number": "94334292963_",
            "expert_profile.registration_number": "2020118181-11_",
            "expert_profile.shop_name": "광주부동산중개_",
        }
        response = self.client.put(
            reverse("profile-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile_name"], "기본프로필_")
        self.assertEqual(response.data["mobile_number"], "010-4334-2929")
        self.assertEqual(response.data["address"], "광주광역시 남구 서문대로 690번길 3_")
        self.assertEqual(response.data["bank_name"], "국민은행_")
        self.assertEqual(response.data["account_number"], "94334292963_")
        self.assertEqual(
            response.data["expert_profile"]["registration_number"], "2020118181-11_")
        self.assertEqual(
            response.data["expert_profile"]["shop_name"], "광주부동산중개_")

    def test_profile_updated_by_random_user(self):
        random_user = CustomUser.objects.create_user(
            username="random", password="psw123123123")
        self.create_expert_profile()
        self.client.force_authenticate(user=None)
        response = self.client.put(reverse("profile-detail", kwargs={"pk": 1}),
                                   {"profile_name": "hacked!!!"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expert_profile_delete(self):
        self.create_expert_profile()
        response = self.client.delete(
            reverse("profile-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AuthedUserTestCase(APITestCase):
    detail_url = reverse("authed-user-detail", args=(1,))

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test",
                                                   email="test@naver.com",
                                                   password="some_strong_password",
                                                   bio="bio",
                                                   name="김상은",
                                                   birthday="1988-05-12")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def create_user(self):
        random_int = str(random.randint(1, 10000000))
        self.user = CustomUser.objects.create_user(username="test"+random_int,
                                                   email="test@naver.com",
                                                   password="some_strong_password",
                                                   bio="bio",
                                                   name="김상은"+random_int,
                                                   birthday="1988-05-12")

    def create_profile(self):
        profile = Profile.objects.create(user=self.user,
                                         profile_name="기본프로필",
                                         mobile_number="010-7777-1618",
                                         address="광주광역시 남구 서문대로 690번길 3",
                                         bank_name="국민은행",
                                         account_number="94334292963")
        return profile

    def test_authed_user_create(self):
        # print(reverse("authed-user-detail", args=(1,)))
        self.create_profile()
        self.create_user()
        self.create_user()

        response = self.client.post(reverse(
            "authed-user-detail", args=(1,)), {"authed_users": [1, 2, 3]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["authed_users"]), 3)
