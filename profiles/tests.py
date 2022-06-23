import json
import os
import random
import shutil
import tempfile
from urllib.request import urlopen

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from addresses.models import Address
from profiles.models import CustomUser, ExpertProfile, Insurance, Profile
from profiles.serializers import ProfileSerializer

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
    "detail": "2층",
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
    "address.detail": "2층",
}


class AllowedUserTestCase(APITestCase):
    detail_url = reverse("allowed-user-detail", args=(1,))
    list_url = reverse("profiles-list")

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
        )

    def setUp(self):
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        self.create_profile()
        self.user1 = self.create_user(1)
        self.create_user(2)

    def create_user(self, id):
        user = CustomUser.objects.create_user(
            email="test" + str(id) + "@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영" + str(id),
            birthday="1955-02-12",
        )
        return user

    def create_profile(self):
        data = {
            "mobile_number": "010-1234-1234",
            "bank_name": 4,
            "account_number": "94334292963",
            **address_form,
        }
        response = self.client.post(self.list_url, data=data)
        return response

    def test_allowed_profile_list(self):
        self.client.post(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": {"email": "test@naver.com"}},
            format="json",
        )
        self.client.post(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": {"email": "test1@naver.com"}},
            format="json",
        )
        profiles = Profile.objects.filter(allowed_user__allowed_users=self.user1).filter(
            is_activated=True
        )
        self.assertEqual(profiles.count(), 1)
        self.token = Token.objects.create(user=self.user1)
        self.api_authentication()
        self.create_profile()
        profiles = Profile.objects.filter(allowed_user__allowed_users=self.user1).filter(
            is_activated=True
        )
        self.assertEqual(profiles.count(), 2)

    def test_allowed_user_create(self):
        # print(reverse("allowed-user-detail", args=(1,)))
        response = self.client.post(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": {"email": "test@naver.com"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("자기 자신의 이메일은 추가할 수 없습니다."))

        response = self.client.post(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": {"email": "test3@naver.com"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("존재하지 않는 이메일 입니다."))

        response = self.client.post(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": {"email": "test1@naver.com"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": {"email": "test2@naver.com"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

        response = self.client.post(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": {"email": "test2@naver.com"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("이미 추가된 회원입니다."))

    def test_allowed_profile_delete(self):
        self.client.post(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": {"email": "test1@naver.com"}},
            format="json",
        )
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.allowed_user.allowed_users.all().count(), 2)

        response = self.client.delete(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": ["test@naver.com"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("자신의 이메일은 삭제할 수 없습니다."))

        response = self.client.delete(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": ["test3@naver.com"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("빠른거래 리스트에 추가되지 않은 회원은 삭제 할 수 없습니다."))

        response = self.client.delete(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": ["test1@naver.com"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(profile.allowed_user.allowed_users.all().count(), 1)
        response = self.client.delete(
            reverse("allowed-user-detail", args=(1,)),
            {"allowed_users": ["test1@naver.com"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("빠른거래 리스트에 추가되지 않은 회원은 삭제 할 수 없습니다."))


MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ExpertProfileTestCase(APITestCase):
    list_url = reverse("profiles-list")

    def _create_image(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            image = Image.new("RGB", (200, 200), "white")
            image.save(f, "PNG")

        return open(f.name, mode="rb")

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
            is_expert=True,
        )

    def setUp(self):
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def test_customuser(self):
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["email"], "test@naver.com")
        self.assertEqual(response.data["is_expert"], True)
        self.assertEqual(response.data["is_staff"], False)
        self.assertEqual(response.data["has_profile"], False)
        self.assertEqual(response.data["bio"], "bio")
        self.assertEqual(response.data["name"], "김주영")
        self.assertEqual(response.data["birthday"], "1955-02-12")

    def create_user_profile(self, id=0, is_expert=False):
        user = CustomUser.objects.create_user(
            email="test" + str(id) + "@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
        )
        address = Address.objects.create(**address_vars)
        profile = Profile.objects.create(
            user=user,
            address=address,
            bank_name=4,
            account_number="98373737372",
            mobile_number="010-9827-111" + str(id),
        )
        if is_expert:
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

    def create_expert_profile(self):
        # FIXME: image removing is not working well.
        image = self._create_image()
        image1 = self._create_image()
        image2 = self._create_image()
        image3 = self._create_image()
        # FIXME: Need to create objects with model directely
        data = {
            "mobile_number": "010-1234-1234",
            "bank_name": 4,
            "account_number": "94334292963",
            **address_form,
            "expert_profile.registration_number": "2020118181-11",
            "expert_profile.shop_name": "광주부동산중개",
            "expert_profile.registration_certificate": image,
            "expert_profile.agency_license": image1,
            "expert_profile.stamp": image2,
            "expert_profile.insurance.image": image3,
            "expert_profile.insurance.from_date": "2021-3-13",
            "expert_profile.insurance.to_date": "2999-3-13",
        }
        response = self.client.post(self.list_url, data=data)
        image.close()
        os.remove(image.name)
        image1.close()
        os.remove(image1.name)
        image2.close()
        os.remove(image2.name)
        image3.close()
        os.remove(image3.name)
        return response

    def test_expert_profile_create(self):
        response = self.create_expert_profile()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["mobile_number"], "010-1234-1234")
        self.assertEqual(response.data["bank_name"], 4)
        self.assertEqual(response.data["account_number"], "94334292963")
        self.assertEqual(
            response.data["address"],
            {
                "id": 1,
                "old_address": "서울 강동구 성내동 111-39",
                "old_address_eng": "111-39, Seongnae-dong, Gangdong-gu, Seoul, Korea",
                "new_address": "서울 강동구 풍성로 87-14",
                "bjdongName": "성내동",
                "bjdongName_eng": "Seongnae-dong",
                "sigunguCd": "11740",
                "bjdongCd": "11740",
                "platGbCd": "",
                "bun": "111",
                "ji": "39",
                "dong": "",
                "ho": "2층",
                "detail": "2층",
            },
        )
        self.assertEqual(response.data["expert_profile"]["registration_number"], "2020118181-11")
        self.assertEqual(response.data["expert_profile"]["shop_name"], "광주부동산중개")
        self.assertEqual(response.data["expert_profile"]["status"], ExpertProfile.REQUEST)
        # FIXME: Need to add image test code

    def test_expert_profile_update(self):
        response = self.create_expert_profile()
        data = {
            "mobile_number": "010-4334-2929",
            "address.ho": "1층",
            "bank_name": 4,
            "account_number": "94334292963_",
            "expert_profile.registration_number": "2020118181-11_",
            "expert_profile.shop_name": "광주부동산중개_",
        }
        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": response.data["id"]}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["mobile_number"], "010-4334-2929")
        self.assertEqual(response.data["address"]["ho"], "1층")
        self.assertEqual(response.data["bank_name"], 4)
        self.assertEqual(response.data["account_number"], "94334292963_")
        self.assertEqual(response.data["expert_profile"]["registration_number"], "2020118181-11_")
        self.assertEqual(response.data["expert_profile"]["shop_name"], "광주부동산중개_")

    def test_approved_expert_profile_update(self):
        response = self.create_expert_profile()
        data = {
            "mobile_number": "010-4334-2929",
            "address.ho": "1층",
            "bank_name": 4,
            "account_number": "94334292963_",
            "expert_profile.registration_number": "2020118181-11_",
            "expert_profile.shop_name": "광주부동산중개_",
        }
        expert_profile = ExpertProfile.objects.get(id=response.data["id"])
        expert_profile.status = ExpertProfile.APPROVED
        expert_profile.save()
        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": response.data["id"]}), data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"].message, _("승인된 전문가 프로필은 수정 할 수 없습니다. 새 프로필을 만드세요.")
        )

    def test_profile_update_unauthenticated(self):
        self.create_expert_profile()
        self.client.force_authenticate(user=None)
        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": 1}), {"bio": "hacked!!!"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expert_profile_update_by_random_user(self):
        random_user = CustomUser.objects.create_user(
            email="random@naver.com", password="psw123123123"
        )
        self.create_expert_profile()
        self.client.force_authenticate(user=random_user)
        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": 1}), {"bio": "hacked!!!"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_expert_profile_delete(self):
        response = self.create_expert_profile()
        response = self.client.delete(reverse("profiles-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_insurance_update(self):
        profile_response = self.create_expert_profile()
        response = self.client.put(
            reverse(
                "profile-insurances-detail",
                kwargs={
                    "profile_pk": profile_response.data["id"],
                    "pk": profile_response.data["expert_profile"]["insurance"]["id"],
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("보증서류 시작일과 종료일을 모두 입력해주세요."))

    def test_approve_expert_post_delete(self):
        expert_profile = self.create_user_profile(is_expert=True)
        self.assertEqual(expert_profile.status, ExpertProfile.REQUEST)
        expert_profile2 = self.create_user_profile(is_expert=True, id=1)
        self.superuser = CustomUser.objects.create_superuser("admin@naver.com", "1234")
        self.token = Token.objects.create(user=self.superuser)
        self.api_authentication()
        response = self.client.put("/api/approve-experts/", data={"profiles": [1]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][1]["status"], ExpertProfile.APPROVED)
        self.assertEqual(response.data["results"][0]["status"], ExpertProfile.REQUEST)
        response = self.client.delete(
            "/api/approve-experts/", data={"profiles": [1]}, format="json"
        )
        self.assertEqual(response.data["results"][1]["status"], ExpertProfile.DENIED)
        self.assertEqual(response.data["results"][0]["status"], ExpertProfile.REQUEST)
        response = self.client.put(
            "/api/approve-experts/", data={"profiles": [1, 2]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][1]["status"], ExpertProfile.APPROVED)
        self.assertEqual(response.data["results"][0]["status"], ExpertProfile.APPROVED)
        response = self.client.delete(
            "/api/approve-experts/", data={"profiles": [1, 2]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][1]["status"], ExpertProfile.DENIED)
        self.assertEqual(response.data["results"][0]["status"], ExpertProfile.DENIED)

    def test_approve_expert_with_no_profiles(self):
        expert_profile = self.create_user_profile(is_expert=True)
        self.assertEqual(expert_profile.status, ExpertProfile.REQUEST)
        expert_profile2 = self.create_user_profile(is_expert=True, id=1)
        self.superuser = CustomUser.objects.create_superuser("admin@naver.com", "1234")
        self.token = Token.objects.create(user=self.superuser)
        self.api_authentication()
        response = self.client.put("/api/approve-experts/", data={"profiles": []}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("전문가가 선택되지 않았습니다."))
        response = self.client.put("/api/approve-experts/", data={"profiles": [3]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("승인 가능한 전문가가 선택되지 않았습니다."))
        response = self.client.delete(
            "/api/approve-experts/", data={"profiles": [5]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("전문가가 선택되지 않았습니다."))


class ProfileTestCase(APITestCase):

    list_url = reverse("profiles-list")
    paper_list = reverse("papers-list")
    mandate_list = reverse("mandates-list")

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
        )
        cls.user1 = CustomUser.objects.create_user(
            email="test1@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
        )

    def setUp(self):
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def create_profile(self):
        data = {
            "mobile_number": "010-1234-1234",
            **address_form,
            "bank_name": 4,
            "account_number": "94334292963",
        }
        response = self.client.post(self.list_url, data=data)
        return response

    def create_expert_profile(self):
        # FIXME: Need to create objects with model directely
        data = {
            "mobile_number": "010-1234-1234",
            "bank_name": 4,
            "account_number": "94334292963",
            **address_form,
            "expert_profile.registration_number": "2020118181-11",
            "expert_profile.shop_name": "광주부동산중개",
            "expert_profile.registration_certificate": self.image,
            "expert_profile.agency_license": self.image1,
            "expert_profile.stamp": self.image2,
            "expert_profile.insurance.image": self.image4,
            "expert_profile.insurance.from_date": "2021-3-13",
            "expert_profile.insurance.to_date": "2022-3-13",
        }
        response = self.client.post(self.list_url, data=data)
        return response

    def test_profile_create(self):
        response = self.create_profile()

    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_count(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.data["count"], 0)
        self.create_profile()
        response = self.client.get(self.list_url)
        self.assertEqual(response.data["count"], 1)

    def test_profile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_retrieve(self):
        self.create_profile()
        response = self.client.get(reverse("profiles-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], "test@naver.com")

    def test_profile_update_by_owner(self):
        self.create_profile()
        data = {
            "mobile_number": "010-4334-2929",
            "address.ho": "1층",
            "bank_name": 20,
            "account_number": "938271122121",
        }
        response = self.client.put(reverse("profiles-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["mobile_number"], "010-4334-2929")
        self.assertEqual(response.data["address"]["ho"], "1층")
        self.assertEqual(response.data["bank_name"], 20)
        self.assertEqual(response.data["account_number"], "938271122121")

    def test_profile_update_by_random_user(self):
        random_user = CustomUser.objects.create_user(
            email="random@naver.com", password="psw123123123"
        )
        self.create_profile()
        self.client.force_authenticate(user=random_user)
        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": 1}), {"bio": "hacked!!!"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_delete(self):
        self.create_profile()
        response = self.client.delete(reverse("profiles-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_profile_update_with_requesting_paper(self):
        response = self.create_profile()
        self.client.force_authenticate(user=self.user1)
        self.create_profile()
        response1 = self.create_profile()
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
                {"profile": response.data["id"], "paper": None, "group": "1"},
                {"profile": response1.data["id"], "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.post(self.paper_list, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(
            reverse("profiles-detail", kwargs={"pk": response1.data["id"]})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_delete_with_paper(self):
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
                {"profile": response.data["id"], "paper": None, "group": "1"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.post(self.paper_list, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Make default profile to False.
        self.create_profile()
        response = self.client.delete(
            reverse("profiles-detail", kwargs={"pk": response.data["id"]})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("요청단계 이후 계약서가 있는 경우 프로필을 삭제할 수 없습니다."))

    def test_profile_update_with_requesting_paper(self):
        response = self.create_profile()
        self.client.force_authenticate(user=self.user1)
        response1 = self.create_profile()
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
                {"profile": response.data["id"], "paper": None, "group": "1"},
                {"profile": response1.data["id"], "paper": None, "group": "2"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.post(self.paper_list, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": response1.data["id"]}),
            data={"mobile_number": "010-1234-5678"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_update_with_paper(self):
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
                {"profile": response.data["id"], "paper": None, "group": "1"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        response = self.client.post(self.paper_list, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": 1}), data={"mobile_number": "010-1234-5678"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("요청단계 이후 계약서가 있는 경우 프로필을 수정할 수 없습니다."))

    def test_profile_update_with_mandate(self):
        response = self.create_profile()
        user = CustomUser.objects.create_user(
            email="test" + str(id) + "@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영" + str(id),
            birthday="1955-02-12",
        )
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
            "address.old_address_eng": "Eng address",
            "address.new_address": "서울 강동구 풍성로 87-14",
            "address.bjdongName": "명도동",
            "address.bjdongName_eng": "Myungdo-dong",
            "address.sigunguCd": "11740",
            "address.bjdongCd": "11740",
            "address.bun": "111",
            "address.ji": "39",
        }
        response = self.client.post(self.mandate_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": 2}), data={"mobile_number": "010-1234-5678"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("작성한 위임장이 있는 경우 프로필을 수정할 수 없습니다."))

    def test_profile_delete_with_mandate(self):
        response = self.create_profile()
        user = CustomUser.objects.create_user(
            email="test" + str(id) + "@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영" + str(id),
            birthday="1955-02-12",
        )
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
            "address.old_address_eng": "Eng address",
            "address.new_address": "서울 강동구 풍성로 87-14",
            "address.bjdongName": "명도동",
            "address.bjdongName_eng": "Myungdo-dong",
            "address.sigunguCd": "11740",
            "address.bjdongCd": "11740",
            "address.bun": "111",
            "address.ji": "39",
        }
        response = self.client.post(self.mandate_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Make default profile to False
        self.create_profile()
        response = self.client.delete(reverse("profiles-detail", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("작성한 위임장이 있는 경우 프로필을 삭제할 수 없습니다."))

    def test_open_profile_list(self):
        self.create_profile()
        user = CustomUser.objects.create_user(
            email="test" + str(id) + "@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영" + str(id),
            birthday="1955-02-12",
        )
        self.token = Token.objects.create(user=user)
        self.api_authentication()
        response = self.client.get(
            "/api/open-profiles/", {"email": "test@naver.com", "mobile_number": "010-1234-1234"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["mobile_number"], "010-1234-12##")
        self.assertEqual(response.data["results"][0]["address"]["old_address"], "서울 강동구 성내동")
        self.assertEqual(response.data["results"][0]["user"]["email"], "##st@naver.com")
        self.assertEqual(response.data["results"][0]["user"]["name"], "김#영")
        response = self.client.get("/api/open-profiles/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("이메일 또는 연락처를 입력해야 합니다."))

    def test_open_profile_detail(self):
        response = self.create_profile()
        response = self.client.get(reverse("open-profile", args=(response.data["id"],)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["mobile_number"], "010-1234-12##")
        self.assertEqual(response.data["address"]["old_address"], "서울 강동구 성내동")
        self.assertEqual(response.data["user"]["email"], "test@naver.com")
        self.assertEqual(response.data["user"]["name"], "김#영")

    def test_set_activated_profile(self):
        response = self.create_profile()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["is_activated"], True)
        response2 = self.create_profile()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["is_activated"], True)
        self.assertEqual(Profile.objects.filter(is_activated=False).count(), 1)

        response = self.client.post(
            reverse("activate-profile", kwargs={"pk": response.data["id"]})
        )
        self.assertEqual(response.data["is_activated"], True)


class CustomUserTestCase(APITestCase):
    profiles_list_url = reverse("profiles-list")

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
        )

    def setUp(self):
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def create_profile(self):
        data = {
            "mobile_number": "010-1234-1234",
            **address_form,
            "bank_name": 4,
            "account_number": "94334292963",
        }
        response = self.client.post(self.profiles_list_url, data=data)
        return response

    def test_customuser(self):
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@naver.com")
        self.assertEqual(response.data["bio"], "bio")
        self.assertEqual(response.data["name"], "김주영")
        self.assertEqual(response.data["birthday"], "1955-02-12")
        self.assertEqual(response.data["is_expert"], False)

    def test_user_update_by_owner(self):
        data = {"birthday": "1955-01-01"}
        response = self.client.put(reverse("user-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["birthday"], "1955-01-01")

    def test_user_update_with_paper(self):
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
                {"profile": response.data["id"], "paper": None, "group": "1"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        self.client.post(reverse("papers-list"), data=data, format="json")

        data = {"birthday": "1955-01-01"}
        response = self.client.put(
            reverse("user-detail", kwargs={"pk": response.data["id"]}), data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"].message, _("요청단계 이후 계약서가 있는 경우 회원 정보를 수정할 수 없습니다.")
        )

    def test_user_delete_with_profile(self):
        self.create_profile()
        data = {"name": "김주영", "email": "test@naver.com"}
        response = self.client.delete(reverse("user-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_delete"], _("탈퇴처리 되었습니다. 계정정보 또한 완전히 삭제되었습니다."))

    def test_user_delete_with_paper(self):
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
                {"profile": response.data["id"], "paper": None, "group": "1"},
            ],
            "security_deposit": 1,
            "special_agreement": "<p>ㅍㅍ</p>",
            "title": "테스트",
            "to_date": "2020-11-30",
            "trade_category": 2,
        }
        self.client.post(reverse("papers-list"), data=data, format="json")
        data = {"name": "김주영", "email": "test@naver.com"}
        response = self.client.delete(
            reverse("user-detail", kwargs={"pk": response.data["id"]}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_delete"], _("탈퇴처리 되었습니다."))

    def test_user_delete_key_error(self):
        data = {"email": "test@naver.com"}
        response = self.client.delete(reverse("user-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("탈퇴할 회원의 정보를 모두 입력해주세요."))

    def test_user_delete_unmatched(self):
        data = {"name": "김주영11", "email": "test@naver.com"}
        response = self.client.delete(reverse("user-detail", kwargs={"pk": 1}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("입력하신 정보가 현재 회원의 정보와 일치하지 않습니다."))


class MandateTestCase(APITestCase):
    mandates_list_url = reverse("mandates-list")
    profile_list_url = reverse("profiles-list")

    def _create_image(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            image = Image.new("RGB", (200, 200), "white")
            image.save(f, "PNG")

        return open(f.name, mode="rb")

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
        )

    def setUp(self):
        self.image = self._create_image()

        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        self.profile1 = self.create_profile().data
        self.profile2 = self.create_user_profile(id=1)
        self.create_mandate()

    def tearDown(self):
        self.image.close()
        os.remove(self.image.name)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT)
        super().tearDownClass()

    def create_profile(self):
        data = {
            "mobile_number": "010-1234-1234",
            **address_form,
            "bank_name": 4,
            "account_number": "94334292963",
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
        address = Address.objects.create(
            old_address="광주 광산구 명도동 169",
            new_address="광주광역시 광산구 가마길 2-21",
            sigunguCd="29170",
            bjdongCd="29170",
            platGbCd="",
            bun="973",
            ji="17",
            dong="202",
            ho="307",
        )
        profile = Profile.objects.create(
            user=user,
            address=address,
            bank_name=4,
            account_number="98373737372",
            mobile_number="010-9827-111" + str(id),
        )
        if is_expert:
            expert_profile = ExpertProfile.objects.create(
                profile=profile, registration_number="2020118181-11", shop_name="효암중개사"
            )
            return expert_profile
        return profile

    def create_mandate(self):
        data = {
            "designator": self.profile1["id"],
            "designee": self.profile2.id,
            "content": "위임내용",
            "from_date": "2020-12-02",
            "to_date": "2020-12-31",
            **address_form,
        }
        return self.client.post(self.mandates_list_url, data=data)

    def test_mandate_create(self):
        response = self.create_mandate()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mandate_retrieve(self):
        response = self.client.get(reverse("mandates-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mandate_update(self):
        response = self.client.get(reverse("mandates-detail", kwargs={"pk": 1}))
        data = {"designator": 1, "designee": 2, "content": "안녕하세요."}
        response = self.client.put(reverse("mandates-detail", kwargs={"pk": 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mandate_update_with_done_status(self):
        data = {
            "designator": 1,
            "designee": 2,
            "designator_signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.put(reverse("mandates-detail", kwargs={"pk": 1}), data=data)

        data = {
            "designator": 1,
            "designee": 2,
            "content": "안녕하세요.",
        }
        response = self.client.put(reverse("mandates-detail", kwargs={"pk": 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("서명이 완료된 위임장은 수정할 수 없습니다."))

    def test_mandate_signature_create(self):
        data = {
            "designator": 1,
            "designee": 2,
            "designator_signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }

        response = self.client.put(reverse("mandates-detail", kwargs={"pk": 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mandate_signature_create_unauthorization(self):
        data = {
            "designator": 1,
            "designee": 2,
            "designator_signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        self.token = Token.objects.create(user=self.profile2.user)
        self.api_authentication()
        response = self.client.put(reverse("mandates-detail", kwargs={"pk": 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mandate_signature_update(self):
        data = {
            "designator": 1,
            "designee": 2,
            "designator_signature": "data:image/png;base64,iVBORw0KGgoBBBBASDFQWERQWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        }

        response = self.client.put(reverse("mandates-detail", kwargs={"pk": 1}), data=data)
        response = self.client.put(reverse("mandates-detail", kwargs={"pk": 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("서명이 완료된 위임장은 수정할 수 없습니다."))

    def test_mandate_signature_delete(self):
        response = self.client.delete(reverse("mandates-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_mandate_signature_delete_with_done_status(self):
        data = {
            "designator": 1,
            "designee": 2,
            "designator_signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAEUCAYAAAAItm20AAAgAElEQVR4Xu3db4xc13nf8d",
        }
        response = self.client.put(reverse("mandates-detail", kwargs={"pk": 1}), data=data)
        response = self.client.delete(reverse("mandates-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].message, _("서명이 완료된 위임장은 삭제할 수 없습니다."))
