import os
import uuid

import phonenumbers
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    PermissionsMixin,
    UserManager,
)
from django.core.mail import send_mail
from django.db import models
from django.db.models import Exists
from django.dispatch import receiver
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from addresses.models import Address


def get_file_path(instance, filename):
    splited_filename = filename.split(".")
    filename = splited_filename[0]
    ext = splited_filename[-1]
    filename = "%s-%s.%s" % (filename, uuid.uuid4(), ext)
    return os.path.join("", filename)


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_expert = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=150)
    birthday = models.DateField(null=True, blank=False)
    bio = models.CharField(max_length=240, blank=True)
    used_count = models.PositiveSmallIntegerField(blank=True, default=0)
    ip_address = models.GenericIPAddressField(null=True)
    average_response_time = models.FloatField(default=0)
    response_rate = models.FloatField(default=0)
    contract_success_rate = models.FloatField(default=0)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def first_profile(self):
        return self.profiles.first()

    @property
    def is_expert_approved(self):
        return self.profiles.filter(
            expert_profile__status=ExpertProfile.APPROVED,
            is_activated=True,
        ).exists()

    class Meta:
        ordering = [
            "-last_login",
        ]


class UserSetting(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_setting")
    is_tour_on = models.BooleanField(default=True)


class Profile(models.Model):
    # 개설기관.표준코드 bank_code_std
    # 리브 앱 참고했으나, 은행이 너무 많아서 아래 링크 참고후 재작성.
    # http://callcenter.kftc.or.kr/finance/finance_info_inquiry.jsp

    BANK_CATEGORY = (
        (0, _("은행명")),
        (2, _("산업은행")),
        (32, _("부산은행")),
        (3, _("기업은행")),
        (34, _("광주은행")),
        (4, _("국민은행")),
        (35, _("제주은행")),
        (7, _("수협")),
        (37, _("전북은행")),
        (11, _("농협은행")),
        (39, _("경남은행")),
        (12, _("지역농축협")),
        (45, _("새마을금고")),
        (20, _("우리은행")),
        (48, _("신용협동조합")),
        (23, _("SC제일은행")),
        (50, _("상호저축은행")),
        (27, _("한국씨티은행")),
        (64, _("산림조합")),
        (81, _("KEB하나은행")),
        (71, _("우체국")),
        (88, _("신한은행")),
        (89, _("K뱅크")),
        (31, _("대구은행")),
        (90, _("카카오뱅크")),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles"
    )
    updated_at = models.DateTimeField(auto_now=True)
    mobile_number = PhoneNumberField()
    address = models.OneToOneField(
        Address, null=True, on_delete=models.SET_NULL, related_name="profile"
    )
    bank_name = models.SmallIntegerField(choices=BANK_CATEGORY, default=0)
    account_number = models.CharField(max_length=45, blank=True)
    is_activated = models.BooleanField(default=True, blank=True)
    # FIXME: Add is_shown_ho for shop_adress to fix displaying not having ho like 2층.

    def __str__(self):
        return self.user.email

    class Meta:
        ordering = ["-is_activated", "-updated_at"]


class Certification(models.Model):
    updated_at = models.DateTimeField(blank=True, null=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="certification")
    imp_uid = models.CharField(max_length=16, blank=True)
    ci = models.CharField(max_length=88, blank=True)  # unique_key
    di = models.CharField(max_length=66, blank=True)  # unique_in_site


class AllowedUser(models.Model):
    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="allowed_users"
    )
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="allowed_user")


class ExpertProfile(models.Model):
    CLOSED = 0
    REQUEST = 1
    APPROVED = 2
    DENIED = 3

    STATUS_CATEGORY = (
        (CLOSED, _("폐업")),
        (REQUEST, _("요청")),
        (APPROVED, _("승인")),
        (DENIED, _("거부")),
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="expert_profile"
    )
    registration_number = models.CharField(max_length=45)
    shop_name = models.CharField(max_length=100)
    registration_certificate = models.ImageField(upload_to=get_file_path)
    agency_license = models.ImageField(upload_to=get_file_path)
    stamp = models.ImageField(upload_to=get_file_path)
    status = models.PositiveSmallIntegerField(choices=STATUS_CATEGORY, default=REQUEST)
    is_shown_ho = models.BooleanField(default=True, null=True)

    class Meta:
        ordering = [
            "-id",
        ]


class Insurance(models.Model):
    expert_profile = models.ForeignKey(
        ExpertProfile, on_delete=models.CASCADE, related_name="insurances"
    )
    image = models.ImageField(upload_to=get_file_path)
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        ordering = [
            "-to_date",
        ]


class Mandate(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="author_mandates",
    )
    updated_at = models.DateTimeField(auto_now=True)
    designator = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="designator_mandates"
    )
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    designee = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="designee_mandates"
    )
    designator_signature = models.TextField(blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    content = models.TextField()

    class Meta:
        ordering = ["-updated_at"]
