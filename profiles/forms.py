from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from addresses.models import Address
from profiles.models import CustomUser, ExpertProfile, Profile, AllowedUser
from django_registration.forms import RegistrationFormUniqueEmail
from datetime import datetime

date_range = 100
this_year = datetime.now().year
User = get_user_model()
class CustomUserForm(RegistrationFormUniqueEmail):
    name = forms.CharField(label=_('이름'), required=True, max_length=150)
    birthday = forms.DateField(label=_('생년월일'), required=True, widget=forms.SelectDateWidget(years=range(this_year - date_range, this_year), attrs = {'class': 'form-control snps-inline-select'}))
    mobile_number = PhoneNumberField(label=_('휴대폰 번호'), required=True)
    bank_name = forms.CharField(label=_('은행명'), required=False, max_length=45)
    account_number = forms.CharField(label=_('계좌번호'), required=False, max_length=45)
    old_address = forms.CharField(label=_('주소'), required=True, max_length=250, widget=forms.TextInput(attrs={"readonly":True, "onfocus":"execDaumPostcode()"}))
    new_address = forms.CharField(required=False, max_length=250, widget=forms.HiddenInput())
    sigunguCd = forms.CharField(required=False, max_length=5, widget=forms.HiddenInput())
    bjdongCd = forms.CharField(required=False, max_length=5, widget=forms.HiddenInput())
    platGbCd = forms.CharField(max_length=1, required=False, widget=forms.HiddenInput())
    bun = forms.CharField(max_length=4, required=False, widget=forms.HiddenInput())
    ji = forms.CharField(max_length=4, required=False, widget=forms.HiddenInput())
    dong = forms.CharField(label=_('동'), required=False, max_length=20)
    ho = forms.CharField(label=_('호'), required=False, max_length=20)

    class Meta(RegistrationFormUniqueEmail.Meta):
        model = CustomUser
        labels = {
            'username': _('아이디')
        }
    @transaction.atomic
    def save(self):
        user = super(CustomUserForm, self).save()
        user.name = self.cleaned_data['name']
        user.birthday = self.cleaned_data['birthday']
        if self.cleaned_data.get('is_expert') == None:
            user.is_expert = False
        else:
            user.is_expert = True
        user.save()
        address = Address.objects.create(old_address=self.cleaned_data['old_address'],
                                         new_address=self.cleaned_data['new_address'],
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
        if user.is_expert:
            ExpertProfile.objects.create(profile=profile,
                                         registration_number=self.cleaned_data['registration_number'],
                                         shop_name=self.cleaned_data['shop_name'],
                                         registration_certificate=self.cleaned_data['registration_certificate'],
                                         agency_license=self.cleaned_data['agency_license'],
                                         stamp=self.cleaned_data['stamp'],
                                         garantee_insurance=self.cleaned_data['garantee_insurance'])
        allowedUser = AllowedUser.objects.create(profile=profile)
        allowedUser.allowed_users.add(user)
        allowedUser.save()
        return user

class ExpertCustomUserForm(CustomUserForm):
    is_expert = forms.BooleanField(label=_('사업자 계정으로 등록하길 원하시면 체크.'), initial=True, required=True, widget=forms.HiddenInput())
    registration_number = forms.CharField(label=_("등록번호"), required=True, max_length=45)
    shop_name = forms.CharField(label=_("상호명"), required=True, max_length=100)
    registration_certificate = forms.ImageField(label=_("중개사 등록증"), required=True)
    agency_license = forms.ImageField(label=_("중개사 자격증"), required=True)
    stamp = forms.ImageField(label=_("인장"), required=True)
    garantee_insurance = forms.ImageField(label=_("보증서류"), required=True)
    old_address = forms.CharField(label=_('사무실 주소'), required=True, max_length=250, widget=forms.TextInput(attrs={"readonly":True, "onfocus":"execDaumPostcode()"}))