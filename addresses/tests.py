from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from addresses.models import Address, Dong
from profiles.models import CustomUser, Profile

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
# Create your tests here.
class DongTestCase(APITestCase):
    list_url = reverse("dongs-list")

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

    def setUp(self):
        self.api_authentication(self.user)

    def test_dong_list(self):
        response = self.client.get(self.list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 202)
        self.assertEqual(Dong.objects.filter(name__contains="서울특별시").count(), 467)
        self.assertEqual(Dong.objects.filter(name__contains="부산광역시").count(), 192)
