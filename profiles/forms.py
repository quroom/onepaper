from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from django.core.validators import RegexValidator
from django import forms
import phonenumbers
from phonenumber_field.formfields import PhoneNumberField
from addresses.models import Address
from profiles.models import AllowedUser, CustomUser, ExpertProfile, Profile, Insurance
from datetime import datetime
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import get_adapter, SignupForm as SocialForm
from django.contrib.auth import password_validation

name_validator = RegexValidator(r"^[가-힣a-zA-Z]+$", _("Your name strings only contain Kor or Eng characters without space."))

date_range = 100
today = datetime.now()
initial_date = datetime(today.year - 30, 1, 1)
User = get_user_model()

class SocialCustomUserForm(SocialForm):
    terms_service = forms.BooleanField(label=_('이용약관 동의'))
    personal_info = forms.BooleanField(label=_('개인정보 처리방침 동의'))
    name = forms.CharField(label=_('성함'), required=True, max_length=150, validators=[name_validator], help_text=_("Your name strings only contain Kor or Eng characters without space."))
    birthday = forms.DateField(label=_('생년월일'), required=True, initial=initial_date, widget=forms.SelectDateWidget(years=range(today.year - date_range, today.year), attrs = {'class': 'form-control snps-inline-select'}))
    mobile_number = PhoneNumberField(label=_('휴대폰 번호'), required=True)
    bank_name = forms.ChoiceField(choices=Profile.BANK_CATEGORY, label=_('은행명'), required=False)
    account_number = forms.CharField(label=_('계좌번호'), required=False, max_length=45)
    old_address = forms.CharField(label=_('주소'), required=True, max_length=250, widget=forms.TextInput(attrs={"readonly":True, "onfocus":"execDaumPostcode()"}))
    old_address_eng = forms.CharField(required=False, max_length=250, widget=forms.HiddenInput())
    new_address = forms.CharField(required=False, max_length=250, widget=forms.HiddenInput())
    bjdongName = forms.CharField(required=False, max_length=20, widget=forms.HiddenInput())
    bjdongName_eng = forms.CharField(required=False, max_length=20, widget=forms.HiddenInput())
    sigunguCd = forms.CharField(required=False, max_length=5, widget=forms.HiddenInput())
    bjdongCd = forms.CharField(required=False, max_length=5, widget=forms.HiddenInput())
    platGbCd = forms.CharField(max_length=1, required=False, widget=forms.HiddenInput())
    bun = forms.CharField(max_length=4, required=False, widget=forms.HiddenInput())
    ji = forms.CharField(max_length=4, required=False, widget=forms.HiddenInput())
    dong = forms.CharField(label=_('동'), required=False, max_length=20)
    ho = forms.CharField(label=_('호'), required=False, max_length=20)

    class Meta:
        model = get_user_model() # use this function for swapping user model

    def __init__(self, *args, **kwargs):
        super(SocialCustomUserForm, self).__init__(*args, **kwargs)
        social_account = kwargs.get('sociallogin').account
        extra_data = social_account.extra_data
        if "name" in extra_data:
            self.fields['name'].initial = extra_data["name"]
        if "mobile" in extra_data:
            self.fields['mobile_number'].initial = extra_data["mobile"]
        if social_account.provider == 'naver':
            if "birthday" in extra_data and "birthyear" in extra_data:
                self.fields['birthday'].initial = datetime(int(extra_data["birthyear"]), int(extra_data["birthday"].split("-")[0]), int(extra_data["birthday"].split("-")[1]))
        if social_account.provider == 'kakao':
            kakao_account = extra_data.get("kakao_account")
            if kakao_account:
                self.fields['name'].initial = kakao_account.get('profile').get('nickname')
                parsed_phone_number = phonenumbers.parse(kakao_account.get('phone_number'))
                self.fields['mobile_number'].initial = phonenumbers.format_number(parsed_phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
                self.fields['birthday'].initial = datetime(int(kakao_account.get("birthyear")), int(kakao_account.get("birthday")[0:2]), int(kakao_account.get("birthday")[2:4]))
        self.fields['email'].widget.attrs['readonly'] = True

    @transaction.atomic
    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.save_user(request, self.sociallogin, form=self)
        email = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.birthday = self.cleaned_data['birthday']
        if self.cleaned_data.get('is_expert') == None:
            user.is_expert = False
        else:
            user.is_expert = True
        user.save()
        address = Address.objects.create(old_address=self.cleaned_data['old_address'],
                                         old_address_eng = self.cleaned_data['old_address_eng'],
                                         new_address=self.cleaned_data['new_address'],
                                         bjdongName=self.cleaned_data['bjdongName'],
                                         bjdongName_eng=self.cleaned_data['bjdongName_eng'],
                                         sigunguCd=self.cleaned_data['sigunguCd'],
                                         bjdongCd=self.cleaned_data['bjdongCd'],
                                         platGbCd=self.cleaned_data['platGbCd'],
                                         bun=self.cleaned_data['bun'],
                                         ji=self.cleaned_data['ji'],
                                         dong=self.cleaned_data['dong'],
                                         ho=self.cleaned_data['ho'])
        profile = Profile.objects.create(user=user,
                                         mobile_number=self.cleaned_data['mobile_number'],
                                         bank_name=self.cleaned_data['bank_name'],
                                         account_number=self.cleaned_data['account_number'],
                                         address=address)
        allowedUser = AllowedUser.objects.create(profile=profile)
        allowedUser.allowed_users.add(user)
        allowedUser.save()

        if user.is_expert:
            return profile
        else:
            return user

class CustomUserForm(SignupForm):
    terms_service = forms.BooleanField(label=_('이용약관 동의'))
    personal_info = forms.BooleanField(label=_('개인정보 처리방침 동의'))
    name = forms.CharField(label=_('성함'), required=True, max_length=150, validators=[name_validator], help_text=_("Your name strings only contain Kor or Eng characters without space."))
    birthday = forms.DateField(label=_('생년월일'), required=True, initial=initial_date, widget=forms.SelectDateWidget(years=range(today.year - date_range, today.year), attrs = {'class': 'form-control snps-inline-select'}))
    mobile_number = PhoneNumberField(label=_('휴대폰 번호'), required=True)
    bank_name = forms.ChoiceField(choices=Profile.BANK_CATEGORY, label=_('은행명'), required=False)
    account_number = forms.CharField(label=_('계좌번호'), required=False, max_length=45)
    old_address = forms.CharField(label=_('주소'), required=True, max_length=250, widget=forms.TextInput(attrs={"readonly":True, "onfocus":"execDaumPostcode()"}))
    old_address_eng = forms.CharField(required=False, max_length=250, widget=forms.HiddenInput())
    new_address = forms.CharField(required=False, max_length=250, widget=forms.HiddenInput())
    bjdongName = forms.CharField(required=False, max_length=20, widget=forms.HiddenInput())
    bjdongName_eng = forms.CharField(required=False, max_length=20, widget=forms.HiddenInput())
    sigunguCd = forms.CharField(required=False, max_length=5, widget=forms.HiddenInput())
    bjdongCd = forms.CharField(required=False, max_length=5, widget=forms.HiddenInput())
    platGbCd = forms.CharField(max_length=1, required=False, widget=forms.HiddenInput())
    bun = forms.CharField(max_length=4, required=False, widget=forms.HiddenInput())
    ji = forms.CharField(max_length=4, required=False, widget=forms.HiddenInput())
    dong = forms.CharField(label=_('동'), required=False, max_length=20)
    ho = forms.CharField(label=_('호'), required=False, max_length=20)

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = password_validation.password_validators_help_text_html()
        self.fields['password2'].help_text = _("Enter the same password as before, for verification.")

    @transaction.atomic
    def save(self, request):
        user = super(CustomUserForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.birthday = self.cleaned_data['birthday']
        if self.cleaned_data.get('is_expert') == None:
            user.is_expert = False
        else:
            user.is_expert = True
        user.save()
        address = Address.objects.create(old_address=self.cleaned_data['old_address'],
                                         old_address_eng = self.cleaned_data['old_address_eng'],
                                         new_address=self.cleaned_data['new_address'],
                                         bjdongName=self.cleaned_data['bjdongName'],
                                         bjdongName_eng=self.cleaned_data['bjdongName_eng'],
                                         sigunguCd=self.cleaned_data['sigunguCd'],
                                         bjdongCd=self.cleaned_data['bjdongCd'],
                                         platGbCd=self.cleaned_data['platGbCd'],
                                         bun=self.cleaned_data['bun'],
                                         ji=self.cleaned_data['ji'],
                                         dong=self.cleaned_data['dong'],
                                         ho=self.cleaned_data['ho'])
        profile = Profile.objects.create(user=user,
                                         mobile_number=self.cleaned_data['mobile_number'],
                                         bank_name=self.cleaned_data['bank_name'],
                                         account_number=self.cleaned_data['account_number'],
                                         address=address)
        allowedUser = AllowedUser.objects.create(profile=profile)
        allowedUser.allowed_users.add(user)
        allowedUser.save()

        if user.is_expert:
            return profile
        else:
            return user

def validate_image(image):
    file_size = image.size
    max_size = 1024*1024
    if file_size > max_size:
        raise ValidationError(_("Max size of file is %(size)s KB"), params={'size': limit_kb})

class ExpertCustomUserForm(CustomUserForm):
    is_expert = forms.BooleanField(label=_('사업자 계정으로 등록하길 원하시면 체크.'), initial=True, required=True, widget=forms.HiddenInput())
    registration_number = forms.CharField(label=_("등록번호"), required=True, max_length=45)
    shop_name = forms.CharField(label=_("상호명"), required=True, max_length=100)
    registration_certificate = forms.ImageField(label=_("중개사무소 등록증"), required=True)
    agency_license = forms.ImageField(label=_("공인중개사 자격증"), required=True)
    stamp = forms.ImageField(label=_("인장"), required=True)
    insurance = forms.ImageField(label=_("보증설정서류"), required=True)
    old_address = forms.CharField(label=_('사무실 주소'), required=True, max_length=250, widget=forms.TextInput(attrs={"readonly":True, "onfocus":"execDaumPostcode()"}))
    from_date = forms.DateField(label=_('보증서류 시작일'), initial=datetime(today.year, today.month, today.day), required=True, widget=forms.SelectDateWidget(years=range(today.year, today.year + date_range), attrs = {'class': 'form-control snps-inline-select'}))
    to_date = forms.DateField(label=_('보증서류 만료일'), initial=datetime(today.year+1, today.month, today.day), required=True, widget=forms.SelectDateWidget(years=range(today.year, today.year + date_range), attrs = {'class': 'form-control snps-inline-select'}))

    def clean_registration_certificate(self):
        image = self.cleaned_data['registration_certificate']
        validate_image(image)
        return image

    def clean_agency_license(self):
        image = self.cleaned_data['agency_license']
        validate_image(image)
        return image

    def clean_stamp(self):
        image = self.cleaned_data['stamp']
        validate_image(image)
        return image

    def clean_insurance(self):
        image = self.cleaned_data['insurance']
        validate_image(image)
        return image

    @transaction.atomic
    def save(self, request):
        profile = super(ExpertCustomUserForm, self).save(request)
        expert_profile = ExpertProfile.objects.create(profile=profile,
                                         registration_number=self.cleaned_data['registration_number'],
                                         shop_name=self.cleaned_data['shop_name'],
                                         registration_certificate=self.cleaned_data['registration_certificate'],
                                         agency_license=self.cleaned_data['agency_license'],
                                         stamp=self.cleaned_data['stamp'])
        Insurance.objects.create(expert_profile=expert_profile,
                            image=self.cleaned_data['insurance'],
                            from_date=self.cleaned_data['from_date'],
                            to_date=self.cleaned_data['to_date'])
        return profile.user