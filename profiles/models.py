import phonenumbers
from django.db import models
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from ipware import get_client_ip

class CustomUser(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True)    
    request_expert = models.BooleanField(blank=True, default=False)
    average_response_time = models.FloatField(default=0)
    response_rate = models.FloatField(default=0)
    contract_success_rate = models.FloatField(default=0)
    bio = models.CharField(max_length=240, blank=True)
    used_count = models.PositiveSmallIntegerField(blank=True, default=0)
    name = models.CharField(max_length=150)
    birthday = models.DateField(null=True)

class Profile(models.Model):
    user = models.ForeignKey(CustomUser,
                             blank=True, null=True,
                             on_delete=models.SET_NULL,
                             related_name="profiles")
    authorization_users = models.ManyToManyField(CustomUser,
                                                 blank=True,
                                                 related_name="auth_profiles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_name = models.CharField(max_length=50)

    #For expert user(like shop)
    shop_name = models.CharField(max_length=100, blank=True)
    shop_address = models.CharField(max_length=200, blank=True)
    registration_number = models.CharField(max_length=45, blank=True)

    #For general user Move name birthday to CustomUser
    mobile_number = PhoneNumberField()
    address = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=45, blank=True)
    account_number = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.user.username + ":" + str(self.profile_name) + ""

#Admin can add user to expert list.
class Expert(models.Model):
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                related_name="expert")
    shop_name = models.CharField(max_length=100, blank=True)
    registration_number = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.user.__str__()
        # return "%s : %s" % (self.profile.user.username, self.profile.profile_name)

class AuthUser(models.Model):
    auth_users = models.ManyToManyField(CustomUser,
                                    blank=True,
                                    related_name="auth_users")
    profile = models.OneToOneField(Profile,
                                    blank=True,
                                    related_name="auth_profile")

@receiver(user_logged_in, sender=CustomUser)
def post_login(sender, user, request, **kwargs):
    client_ip, is_routable = get_client_ip(request)
    user.ip_address = client_ip
    user.save()