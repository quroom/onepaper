import shutil
import tempfile

from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from PIL import Image
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from addresses.models import Address
from listings.models import AskListing, Listing, ListingAddress
from profiles.models import CustomUser, ExpertProfile, Insurance, Profile

# Create your tests here.
MEDIA_ROOT = tempfile.mkdtemp()
today = timezone.localtime().date()

# FIXME: Move to class , because of duplicated.
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

asklisting_data = {
    "location": "광주광역시 동구 계림동",
    "online_visit": True,
    "term_of_lease": 12,
    "item_category": 1,
    "trade_category": 1,
    "security_deposit": 200,
    "monthly_fee": 30,
    "maintenance_fee": 5,
    "visit_date": today,
    "moving_date": today.replace(year=today.year + 1),
    "content": "테스트 코드 입니다.",
}


class AskListingTestCase(APITestCase):
    list_url = reverse("asklistings-list")

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

        AskListing.objects.create(author=cls.user, **asklisting_data)
        AskListing.objects.create(author=cls.user, **asklisting_data)

        cls.expert_user = CustomUser.objects.create_user(
            email="expert@naver.com",
            password="some_strong_password",
            bio="bio",
            name="서주은",
            birthday="1955-02-12",
            is_expert=True,
        )
        address = Address.objects.create(**address_vars)
        profile2 = Profile.objects.create(
            user=cls.expert_user,
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
        AskListing.objects.create(author=cls.expert_user, **asklisting_data)

    def setUp(self):
        self.api_authentication(self.user)

    def test_asklisting_create(self):
        response = self.client.post(self.list_url, data=asklisting_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["location"], "광주광역시 동구 계림동")

    def test_asklisting_list(self):
        response = self.client.get(self.list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["monthly_fee"], 30)

    def test_asklisting_with_expert(self):
        self.api_authentication(self.expert_user)
        response = self.client.post(self.list_url, data=asklisting_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 4)

        response = self.client.put(
            reverse("asklistings-detail", kwargs={"pk": 1}),
            data={"monthly_fee": 50},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(reverse("asklistings-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_asklisting_detail_and_update(self):
        response = self.client.get(reverse("asklistings-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["monthly_fee"], 30)

        response = self.client.get(reverse("asklistings-detail", kwargs={"pk": 3}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.put(
            reverse("asklistings-detail", kwargs={"pk": 1}),
            data={"monthly_fee": 50},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["monthly_fee"], 50)

    def test_asklisting_delete(self):
        response = self.client.delete(reverse("asklistings-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.list_url, format="json")
        self.assertEqual(response.data["count"], 1)

    def test_asklisting_without_profile(self):
        # Create
        user_no_profile = CustomUser.objects.create_user(
            email="test9@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김주영",
            birthday="1955-02-12",
        )

        self.api_authentication(user=user_no_profile)
        response = self.client.post(self.list_url, data=asklisting_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(self.list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ListingTestCase(APITestCase):
    listing_data = {
        "listingaddress.old_address": "광주 광산구 명도동 169",
        "listingaddress.old_address_eng": "169, Myeongdo-dong, Gwangsan-gu, Gwangju, Korea",
        "listingaddress.new_address": "광주 광산구 명도동 169",
        "listingaddress.bjdongName": "명도동",
        "listingaddress.bjdongName_eng": "Myeongdo-dong",
        "listingaddress.sigunguCd": "29200",
        "listingaddress.bjdongCd": "29200",
        "listingaddress.bun": "169",
        "listingaddress.ji": "",
        "listingaddress.dong": "",
        "listingaddress.ho": "",
        "title": "매물 업로드 데이터 보기 위함",
        "down_payment": 200,
        "security_deposit": 500,
        "maintenance_fee": 5,
        "monthly_fee": 30,
        "content": "감사합니다",
        "item_category": 1,
        "trade_category": 1,
        "online_visit": False,
        "minimum_period": 12,
    }
    _local_listing_data = {
        "title": "매물 업로드 데이터 보기 위함",
        "down_payment": 200,
        "security_deposit": 500,
        "maintenance_fee": 5,
        "monthly_fee": 30,
        "content": "감사합니다",
        "item_category": 1,
        "trade_category": 1,
        "online_visit": False,
        "minimum_period": 12,
    }
    list_url = reverse("listings-list")

    def _create_image(self, width=None, height=None):
        if width and height:
            with tempfile.NamedTemporaryFile(dir=MEDIA_ROOT, suffix=".png", delete=False) as f:
                image = Image.new("RGB", (width, height), "white")
                image.save(f, "PNG")
        else:
            with tempfile.NamedTemporaryFile(dir=MEDIA_ROOT, suffix=".png", delete=False) as f:
                image = Image.new("RGB", (200, 200), "white")
                image.save(f, "PNG")

        return open(f.name, mode="rb")

    def api_authentication(self, user):
        self.token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def setUp(self):
        self.images = []
        for i in range(0, 10):
            self.images.append(self._create_image())

        for index, image in enumerate(self.images):
            self.listing_data["images[" + str(index) + "]image"] = image
            if index == 0:
                self.listing_data["images[" + str(index) + "]is_default"] = True
            else:
                self.listing_data["images[" + str(index) + "]is_default"] = False

        self.user = CustomUser.objects.create(
            email="test@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김테스트",
            birthday="1955-02-02",
        )
        address = Address.objects.create(**address_vars)
        Profile.objects.create(
            user=self.user,
            address=address,
            bank_name=34,
            account_number="120982711",
            mobile_number="010-1234-5678",
        )

        self.user1 = CustomUser.objects.create(
            email="test1@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김테스트1",
            birthday="1999-02-02",
        )
        address = Address.objects.create(**address_vars)
        Profile.objects.create(
            user=self.user1,
            address=address,
            bank_name=34,
            account_number="120982711",
            mobile_number="010-1234-5678",
        )
        self.api_authentication(self.user)

        listing = Listing.objects.create(author=self.user, **self._local_listing_data)
        ListingAddress.objects.create(listing=listing, **address_vars)

    def tearDown(self):
        for image in self.images:
            image.close()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT)
        super().tearDownClass()

    def test_listing_create(self):
        response = self.client.post(self.list_url, data=self.listing_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["down_payment"], 200)
        self.assertEqual(response.data["images"][0]["is_default"], True)

    def test_listing_create_with_no_profile_user(self):
        user = CustomUser.objects.create(
            email="test2@naver.com",
            password="some_strong_password",
            bio="bio",
            name="김테스트1",
            birthday="1999-02-02",
        )
        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url, data=self.listing_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listing_create_with_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "error")
        response = self.client.post(self.list_url, data=self.listing_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listing_create_with_overflow_images(self):
        data = self.listing_data.copy()
        image_length = len(self.images)
        data["images[" + str(image_length) + "]image"] = self._create_image()
        data["images[" + str(image_length) + "]is_default"] = False
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["image"][0], _("이미지는 10개까지 첨부할 수 있습니다."))

    def test_listing_create_with_big_image(self):
        data = self.listing_data.copy()
        image_length = len(self.images)
        data["images[" + str(image_length - 1) + "]image"] = self._create_image(1024, 1025)
        data["images[" + str(image_length - 1) + "]is_default"] = False
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["image"][0], _("이미지 해상도 초과입니다. 최대 1024x1024까지 지원합니다."))

    def test_listing_update(self):
        create_response = self.client.post(self.list_url, data=self.listing_data)
        data = {
            "listingaddress.old_address": "광주 광산구 명도동 169",
            "listingaddress.old_address_eng": "169, Myeongdo-dong, Gwangsan-gu, Gwangju, Korea",
            "listingaddress.new_address": "광주 광산구 명도동 169",
            "listingaddress.bjdongName": "명도동",
            "listingaddress.bjdongName_eng": "Myeongdo-dong",
            "listingaddress.sigunguCd": "29200",
            "listingaddress.bjdongCd": "29200",
            "listingaddress.bun": "169",
            "listingaddress.ji": "",
            "listingaddress.dong": "",
            "listingaddress.ho": "",
            "title": "매물 업로드 데이터 보기 위함",
            "down_payment": 100,
            "security_deposit": 200,
            "maintenance_fee": 10,
            "monthly_fee": 20,
            "content": "감사합니다",
            "item_category": 1,
            "trade_category": 1,
            "online_visit": False,
            "minimum_period": 12,
            "images[0]id": create_response.data["images"][5]["id"],
            "images[0]is_default": True,
            "images[1]id": create_response.data["images"][4]["id"],
            "images[1]is_deleted": True,
        }
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        response = self.client.put(
            reverse("listings-detail", kwargs={"pk": create_response.data["id"]}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for image in response.data["images"]:
            is_deleted_passed = True
            if image["id"] == create_response.data["images"][5]["id"]:
                self.assertEqual(image["is_default"], True)
            elif image["id"] == create_response.data["images"][4]["id"]:
                is_deleted_passed = False
                self.assertEqual(image["is_default"], False)
            else:
                self.assertEqual(image["is_default"], False)
        self.assertEqual(response.data["listingaddress"]["old_address"], "광주 광산구 명도동 169")
        self.assertEqual(response.data["listingaddress"]["new_address"], "광주 광산구 명도동 169")
        self.assertEqual(len(response.data["images"]), len(create_response.data["images"]) - 1)
        self.assertEqual(is_deleted_passed, True)
        self.assertEqual(response.data["down_payment"], 100)
        self.assertEqual(response.data["security_deposit"], 200)
        self.assertEqual(response.data["maintenance_fee"], 10)
        self.assertEqual(response.data["monthly_fee"], 20)
        self.assertEqual(response.data["status"], 1)
        response = self.client.put(
            reverse("update-status", kwargs={"pk": create_response.data["id"]}), data={"status": 0}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 0)
        response = self.client.put(
            reverse("update-status", kwargs={"pk": create_response.data["id"]}), data={"status": 1}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 1)

    def test_listing_updated_delete_errors(self):
        create_response = self.client.post(self.list_url, data=self.listing_data)
        data = {
            "listingaddress.old_address": "광주 광산구 명도동 169",
            "listingaddress.old_address_eng": "169, Myeongdo-dong, Gwangsan-gu, Gwangju, Korea",
            "listingaddress.new_address": "광주 광산구 명도동 169",
            "listingaddress.bjdongName": "명도동",
            "listingaddress.bjdongName_eng": "Myeongdo-dong",
            "listingaddress.sigunguCd": "29200",
            "listingaddress.bjdongCd": "29200",
            "listingaddress.bun": "169",
            "listingaddress.ji": "",
            "listingaddress.dong": "",
            "listingaddress.ho": "",
            "title": "매물 업로드 데이터 보기 위함",
            "down_payment": 100,
            "security_deposit": 200,
            "maintenance_fee": 10,
            "monthly_fee": 20,
            "content": "감사합니다",
            "item_category": 1,
            "trade_category": 1,
            "online_visit": False,
            "minimum_period": 12,
        }
        invalid_id = 55
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        data["images[0]id"] = invalid_id
        data["images[0]is_deleted"] = True
        data["images[1]id"] = 1
        data["images[1]is_deleted"] = True
        # PUT with unavailable ID
        response = self.client.put(
            reverse("listings-detail", kwargs={"pk": create_response.data["id"]}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], _("존재하지 않는 이미지(ID:%(id)d)입니다.") % {"id": invalid_id}
        )

        self.client.force_authenticate(user=self.user1)
        data = {
            "listingaddress.old_address": "광주 광산구 명도동 169",
            "listingaddress.old_address_eng": "169, Myeongdo-dong, Gwangsan-gu, Gwangju, Korea",
            "listingaddress.new_address": "광주 광산구 명도동 169",
            "listingaddress.bjdongName": "명도동",
            "listingaddress.bjdongName_eng": "Myeongdo-dong",
            "listingaddress.sigunguCd": "29200",
            "listingaddress.bjdongCd": "29200",
            "listingaddress.bun": "169",
            "listingaddress.ji": "",
            "listingaddress.dong": "",
            "listingaddress.ho": "",
            "title": "매물 업로드 데이터 보기 위함",
            "down_payment": 100,
            "security_deposit": 200,
            "maintenance_fee": 10,
            "monthly_fee": 20,
            "content": "감사합니다",
            "item_category": 1,
            "trade_category": 1,
            "online_visit": False,
            "minimum_period": 12,
        }

        # PUT with no images
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], _("하나 이상의 이미지를 첨부하여야 합니다."))
        # PUT with unauthorized user
        response = self.client.put(
            reverse("listings-detail", kwargs={"pk": create_response.data["id"]}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # DELETE with unauthorized user
        response = self.client.delete(
            reverse("listings-detail", kwargs={"pk": create_response.data["id"]}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
