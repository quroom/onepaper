from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from profiles.models import CustomUser
from django_registration.forms import RegistrationForm
from datetime import datetime

date_range = 100
this_year = datetime.now().year
class CustomUserForm(RegistrationForm):    
    # username = forms.CharField(label=_('widget=forms.TextInput(attrs={'autofocus': True}))
    name = forms.CharField(label=_('이름'), required=True, max_length=150)
    birthday = forms.DateField(label=_('생년월일'), required=True, widget=forms.SelectDateWidget(years=range(this_year - date_range, this_year), attrs = {'class': 'form-control snps-inline-select'}))
    request_expert = forms.BooleanField(label=_('중개사 계정으로 등록하길 원하시면 체크.'), initial=False, required=False)
    
    class Meta(RegistrationForm.Meta):
        model = CustomUser
        labels = {
            'username': _('아이디')
        }
    def save(self):
        user = super(CustomUserForm, self).save()
        user.name = self.cleaned_data['name']
        user.birthday = self.cleaned_data['birthday']
        user.request_expert = self.cleaned_data['request_expert']
        user.save()
        return user