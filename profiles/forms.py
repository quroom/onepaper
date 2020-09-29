from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from profiles.models import CustomUser
from django_registration.forms import RegistrationForm

class CustomUserForm(RegistrationForm):    
    # username = forms.CharField(label=_('widget=forms.TextInput(attrs={'autofocus': True}))
    name = forms.CharField(label=_('이름'), required=True, max_length=150)
    birthday = forms.DateField(label=_('생년월일'), required=True, widget=forms.SelectDateWidget(attrs = {'class': 'form-control snps-inline-select'}))
    
    class Meta(RegistrationForm.Meta):
        model = CustomUser
        labels = {
            'username': _('아이디')
        }