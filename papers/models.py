from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile

class Paper(models.Model):
    ONE_ROOM = 1
    TWO_ROOM = 2
    THREE_ROOM = 3
    FOUR_ROOM = 4
    SHARE_HOUSE = 5
    OFFICE_TEL = 6
    APARTMENT = 20
    VILLA = 21
    HOUSE = 22
    COMMERCIAL_HOUSE = 23
    STORE = 40
    LAND = 41
    ITEM_TYPE = (
        (ONE_ROOM, '원룸'),
        (TWO_ROOM, '투룸'),
        (THREE_ROOM, '쓰리룸'),
        (FOUR_ROOM, '포룸'),
        (SHARE_HOUSE, '쉐어하우스'),
        (OFFICE_TEL, '오피스텔'),

        (APARTMENT, '아파트'),
        (VILLA, '빌라'),
        (HOUSE, '단독주택'),
        (COMMERCIAL_HOUSE, '상가주택'),

        (STORE, '상가'),
        (LAND, '토지'),
    )

    # TR(TRADE) DL(Deposit Loan) RT(Rent) EX(Exchange) CS(Consulting)
    RENT = 1
    DEPOSIT_LOAN = 2
    TRADE = 3
    EXCAHNGE = 4
    TRADE_TYPE = (
        (RENT, '월세'),
        (DEPOSIT_LOAN, '전세'),
        (TRADE, '매매'),
        (EXCAHNGE, '교환'),
    )

    DRAFT = 1
    DONE = 2
    HIDDEN = 3
    STATUS_TYPE = (
        (DRAFT, '작성중'),
        (DONE, '완료'),
        (HIDDEN, '숨김')
    )

    # Need to be moved to Realestates model.
    ground_type = models.CharField(max_length=10)
    lot_area = models.PositiveSmallIntegerField(default=0, blank=True)
    building_structure = models.CharField(max_length=100)
    building_type = models.CharField(max_length=100)
    building_area = models.SmallIntegerField(default=0, blank=True)

    author = models.ForeignKey(User,
                               null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name="author_papers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    trade_type = models.PositiveSmallIntegerField(
        choices=TRADE_TYPE, default=RENT)
    address = models.CharField(max_length=250)
    realestate_type = models.PositiveSmallIntegerField(
        choices=ITEM_TYPE, default=ONE_ROOM)
    security_deposit = models.BigIntegerField(null=True, blank=True)
    down_payment = models.BigIntegerField(null=True, blank=True)
    monthly_fee = models.PositiveIntegerField(null=True, blank=True)
    maintenance_fee = models.PositiveIntegerField(null=True, blank=True)
    special_agreement = models.TextField(blank=True)
    expert = models.ForeignKey(Profile,
                               null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name="expert_papers")
    seller = models.ForeignKey(Profile,
                               null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name="seller_papers")
    buyer = models.ForeignKey(Profile,
                              null=True, blank=True,
                              on_delete=models.SET_NULL,
                              related_name="buyer_papers")
    expert_signature = models.ImageField(null=True, blank=True)
    seller_signature = models.ImageField(null=True, blank=True)
    buyer_signature = models.ImageField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_TYPE, default=DRAFT)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.title