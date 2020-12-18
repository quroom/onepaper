from django.db.models import Exists
import phonenumbers
from addresses.models import Address
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

class CustomUser(AbstractUser):
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True)
    average_response_time = models.FloatField(default=0)
    response_rate = models.FloatField(default=0)
    contract_success_rate = models.FloatField(default=0)
    used_count = models.PositiveSmallIntegerField(blank=True, default=0)
    name = models.CharField(max_length=150)
    birthday = models.DateField(null=True, blank=False)
    is_expert = models.BooleanField(default=False)
    bio = models.CharField(max_length=240, blank=True)

class Profile(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name="profiles")
    updated_at = models.DateTimeField(auto_now=True)
    mobile_number = PhoneNumberField()
    address = models.OneToOneField(Address,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name="profile")
    bank_name = models.CharField(max_length=45, blank=True)
    account_number = models.CharField(max_length=45, blank=True)
    is_default = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-is_default',)

class AllowedUser(models.Model):
    allowed_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name="allowed_users")
    profile = models.OneToOneField(Profile,
                                   on_delete=models.CASCADE,
                                   related_name="allowed_user")

class ExpertProfile(models.Model):
    REQUEST = 0
    APPROVED = 1
    DENIED = 2
    CLOSED = 3

    STATUS_CATEGORY = (
        (REQUEST, _('요청')),
        (APPROVED, _('승인')),
        (DENIED, _('거부')),
        (CLOSED, _('폐업'))
    )

    profile = models.OneToOneField(Profile,
                             on_delete=models.CASCADE,
                             related_name="expert_profile")
    updated_at = models.DateTimeField(auto_now=True)

    registration_number = models.CharField(max_length=45)
    shop_name = models.CharField(max_length=100)

    registration_certificate = models.ImageField()
    agency_license = models.ImageField()
    stamp = models.ImageField()
    garantee_insurance = models.ImageField()
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CATEGORY, default=REQUEST)

    class Meta:
        ordering = ('id',)

class Mandate(models.Model):
    author = models.ForeignKey(CustomUser,
                               null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name="author_mandates")
    updated_at = models.DateTimeField(auto_now=True)
    designator = models.ForeignKey(Profile,
                            on_delete=models.CASCADE,
                            related_name="designator")
    address = models.OneToOneField(Address,
                                   on_delete=models.CASCADE)
    designee = models.ForeignKey(Profile,
                            on_delete=models.CASCADE,
                            related_name="designee")
    designator_signature = models.ImageField(blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    content = models.TextField()

    class Meta:
        ordering = ['-updated_at']