from datetime import datetime

import phonenumbers
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialForm
from allauth.socialaccount.forms import get_adapter
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from addresses.models import Address
from profiles.models import AllowedUser, CustomUser, ExpertProfile, Insurance, Profile, UserSetting

name_validator = RegexValidator(
    r"^[가-힣a-zA-Z]+$", _("Your name strings only contain Kor or Eng characters without space.")
)

date_range = 100
today = datetime.now()
initial_date = datetime(today.year - 30, 1, 1)
User = get_user_model()


class SocialCustomUserForm(SocialForm):
    terms_service = forms.BooleanField(
        label=_("이용약관 동의"), initial=True, widget=forms.HiddenInput()
    )
    personal_info = forms.BooleanField(
        label=_("개인정보 처리방침 동의"), initial=True, widget=forms.HiddenInput()
    )
    name = forms.CharField(
        label=_("성함"),
        required=True,
        max_length=150,
        validators=[name_validator],
        help_text=_("Your name strings only contain Kor or Eng characters without space."),
    )
    birthday = forms.DateField(
        label=_("생년월일"),
        required=True,
        initial=initial_date,
        widget=forms.SelectDateWidget(
            years=range(today.year - date_range, today.year),
            attrs={"class": "form-control snps-inline-select"},
        ),
    )

    class Meta:
        model = get_user_model()  # use this function for swapping user model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].disabled = True

    @transaction.atomic
    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.save_user(request, self.sociallogin, form=self)
        user.name = self.cleaned_data["name"]
        user.birthday = self.cleaned_data["birthday"]
        if self.cleaned_data.get("is_expert") == None:
            user.is_expert = False
        else:
            user.is_expert = True
        user.save()
        UserSetting.objects.create(user=user)
        return user


class CustomUserForm(SignupForm):
    terms_service = forms.BooleanField(
        label=_("이용약관 동의"), initial=True, widget=forms.HiddenInput()
    )
    personal_info = forms.BooleanField(
        label=_("개인정보 처리방침 동의"), initial=True, widget=forms.HiddenInput()
    )
    name = forms.CharField(
        label=_("성함"),
        required=True,
        max_length=150,
        validators=[name_validator],
        help_text=_("Your name strings only contain Kor or Eng characters without space."),
    )
    birthday = forms.DateField(
        label=_("생년월일"),
        required=True,
        initial=initial_date,
        widget=forms.SelectDateWidget(
            years=range(today.year - date_range, today.year),
            attrs={"class": "form-control snps-inline-select"},
        ),
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields[
            "password1"
        ].help_text = password_validation.password_validators_help_text_html()
        self.fields["password2"].help_text = _(
            "Enter the same password as before, for verification."
        )

    @transaction.atomic
    def save(self, request):
        user = super(CustomUserForm, self).save(request)
        user.name = self.cleaned_data["name"]
        user.birthday = self.cleaned_data["birthday"]
        user.terms_service = True
        user.personal_info = True
        if self.cleaned_data.get("is_expert") == None:
            user.is_expert = False
        else:
            user.is_expert = True
        user.save()
        UserSetting.objects.create(user=user)
        return user


def validate_image(image):
    file_size = image.size
    max_size = 1024 * 1024
    if file_size > max_size:
        raise ValidationError(_("Max size of file is %(size)s KB"), params={"size": max_size})


class ExpertCustomUserForm(CustomUserForm):
    is_expert = forms.BooleanField(
        label=_("사업자 계정으로 등록하길 원하시면 체크."), initial=True, required=True, widget=forms.HiddenInput()
    )

    @transaction.atomic
    def save(self, request):
        return super(ExpertCustomUserForm, self).save(request)
