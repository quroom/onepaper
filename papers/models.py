from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from profiles.models import CustomUser, Expert, Profile

class Paper(models.Model):
    ONEROOM = 1
    TWOROOM = 2
    THREEROOM = 3
    FOURROOM = 4
    SHAREHOUSE = 5
    OFFICETEL = 6

    APARTMENT = 20
    VILLA = 21
    HOUSE = 22
    COMMERCIALHOUSE = 23

    STORE = 40
    LAND = 41
    ITEM_TYPE = (
        (ONEROOM, _('원룸')),
        (TWOROOM, _('투룸')),
        (THREEROOM, _('쓰리룸')),
        (FOURROOM, _('포룸')),
        (SHAREHOUSE, _('쉐어하우스')),
        (OFFICETEL, _('오피스텔')),

        (APARTMENT, _('아파트')),
        (VILLA, _('빌라')),
        (HOUSE, _('단독주택')),
        (COMMERCIAL_HOUSE, _('상가주택')),

        (STORE, _('상가')),
        (LAND, _('토지')),
    )

    # TR(TRADE) DL(Deposit Loan) RT(Rent) EX(Exchange) CS(Consulting)
    RENT = 1
    DEPOSITLOAN = 2
    TRADE = 3
    EXCAHNGE = 4
    TRADE_TYPE = (
        (RENT, _('월세')),
        (DEPOSITLOAN, _('전세')),
        (TRADE, _('매매')),
        (EXCAHNGE, _('교환')),
    )

    DRAFT = 0
    DONE = 1
    HIDDEN = 2
    STATUS_TYPE = (
        (DRAFT, _('작성중')),
        (DONE, _('완료')),
        (HIDDEN, _('숨김'))
    )

    # Need to be moved to Realestates model.
    ground_type = models.CharField(max_length=10)
    lot_area = models.PositiveSmallIntegerField(default=0, blank=True)
    building_structure = models.CharField(max_length=100)
    building_type = models.CharField(max_length=100)
    building_area = models.SmallIntegerField(default=0, blank=True)

    author = models.ForeignKey(CustomUser,
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
    down_payment = models.BigIntegerField(null=True, blank=True)
    security_deposit = models.BigIntegerField()
    monthly_fee = models.PositiveIntegerField()
    maintenance_fee = models.PositiveIntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    special_agreement = models.TextField(blank=True)
    expert = models.ForeignKey(Profile,
                               null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name="expert_papers")
    seller = models.ForeignKey(Profile,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name="seller_papers")
    buyer = models.ForeignKey(Profile,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name="buyer_papers")
    status = models.PositiveSmallIntegerField(
        choices=STATUS_TYPE, default=DRAFT)

    def __str__(self):
        return self.title

    def full_clean(self):
        expert_user = getattr(self.expert,'user')
        seller_user = getattr(self.seller,'user')
        buyer_user = getattr(self.buyer,'user')
        if expert_user==seller_user or expert_user==buyer_user or seller_user==buyer_user:
            raise ValidationError({
                'expert':_('같은 회원은 입력될 수 없습니다.'),
                'seller':_('같은 회원은 입력될 수 없습니다.'),
                'buyer':_('같은 회원은 입력될 수 없습니다.'),
            })

class Signature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paper_visible = models.BooleanField(default=True)
    paper = models.ForeignKey(Paper,
                                 on_delete=models.CASCADE,
                                 related_name="paper_signatures")
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name="profile_signatures")
    signature = models.ImageField()

    class Meta:
        unique_together = ('paper', 'profile')

    def __str__(self):
        return str(self.profile)