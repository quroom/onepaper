from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from profiles.models import CustomUser
from django_registration.forms import RegistrationFormUniqueEmail
from datetime import datetime

date_range = 100
this_year = datetime.now().year
User = get_user_model()
class CustomUserForm(RegistrationFormUniqueEmail):
    name = forms.CharField(label=_('이름'), required=True, max_length=150)
    birthday = forms.DateField(label=_('생년월일'), required=True, widget=forms.SelectDateWidget(years=range(this_year - date_range, this_year), attrs = {'class': 'form-control snps-inline-select'}))
    is_expert = forms.BooleanField(label=_('사업자 계정으로 등록하길 원하시면 체크.'), initial=False, required=False)
    mobile_number = PhoneNumberField(label=_('휴대폰 번호'), required=True)
    address = forms.CharField(label=_('주소'), required=True, max_length=250)
    dong = forms.CharField(label=_('동'), required=False, max_length=20)
    ho = forms.CharField(label=_('호'), required=False, max_length=20)

    class Meta(RegistrationFormUniqueEmail.Meta):
        model = CustomUser
        labels = {
            'username': _('아이디')
        }
    def save(self):
        user = super(CustomUserForm, self).save()
        user.name = self.cleaned_data['name']
        user.birthday = self.cleaned_data['birthday']
        user.is_expert = self.cleaned_data['is_expert']
        user.save()
        return user