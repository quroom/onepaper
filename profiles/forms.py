from profiles.models import CustomUser
from django_registration.forms import RegistrationForm

class CustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = CustomUser