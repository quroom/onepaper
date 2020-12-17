from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from profiles.models import CustomUser
from django_registration.forms import RegistrationForm, RegistrationFormUniqueEmail, validators
from datetime import datetime

date_range = 100
this_year = datetime.now().year
User = get_user_model()
class CustomUserForm(RegistrationForm):
    # username = forms.CharField(label=_('widget=forms.TextInput(attrs={'autofocus': True}))
    name = forms.CharField(label=_('이름'), required=True, max_length=150)
    birthday = forms.DateField(label=_('생년월일'), required=True, widget=forms.SelectDateWidget(years=range(this_year - date_range, this_year), attrs = {'class': 'form-control snps-inline-select'}))
    is_expert = forms.BooleanField(label=_('사업자 계정으로 등록하길 원하시면 체크.'), initial=False, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        email_field = User.get_email_field_name()
        self.fields[email_field].validators.append(
            validators.CaseInsensitiveUnique(
                User, email_field, _("이메일은 이미 사용중입니다. 다른 이메일을 입력 해주세요.")
            )
        )

    class Meta(RegistrationForm.Meta):
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