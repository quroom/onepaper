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
    average_response_time = models.FloatField(default=0)
    response_rate = models.FloatField(default=0)
    contract_success_rate = models.FloatField(default=0)
    bio = models.CharField(max_length=240, blank=True)
    used_count = models.PositiveSmallIntegerField(blank=True, default=0)

class Profile(models.Model):
    user = models.ForeignKey(CustomUser,
                             blank=True, null=True,
                             on_delete=models.SET_NULL,
                             related_name="profiles")
    authorization_users = models.ManyToManyField(CustomUser, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_name = models.CharField(max_length=50, blank=False)

    #For expert user(like shop)
    shop_name = models.CharField(max_length=100, blank=True)
    shop_address = models.CharField(max_length=200, blank=True)
    register_number = models.CharField(max_length=45, blank=True)

    #For general user
    name = models.CharField(max_length=150, blank=True)
    birthday = models.DateField(null=True, blank=True)
    mobile_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    bank_name = models.CharField(max_length=45, blank=True)
    account_number = models.CharField(max_length=45, blank=True)
    used_count = models.PositiveSmallIntegerField(blank=True, default=0)

    def __str__(self):
        return self.user.username + ":" + str(self.profile_name) + ""


@receiver(user_logged_in, sender=CustomUser)
def post_login(sender, user, request, **kwargs):
    client_ip, is_routable = get_client_ip(request)
    user.ip_address = client_ip
    user.save()