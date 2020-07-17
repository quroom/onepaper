from django.db import models
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from ipware import get_client_ip

class Profile(models.Model):
    user = models.OneToOneField(User,
                                blank=True, null=True,
                                on_delete=models.SET_NULL,
                                unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150, blank=True)
    birthday = models.DateField(null=True, blank=True)
    mobile_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    bank_name = models.CharField(max_length=45, blank=True)
    account_number = models.CharField(max_length=45, blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    average_response_time = models.FloatField(default=0)
    response_rate = models.FloatField(default=0)
    contract_success_rate = models.FloatField(default=0)
    bio = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return self.user.username

class Expert(models.Model):
    profile = models.OneToOneField(Profile,
                                blank=True, null=True,
                                on_delete=models.SET_NULL,
                                related_name="expert"
                                )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    register_number = models.CharField(max_length=45, blank=True)
    shop_name = models.CharField(max_length=100, blank=True)
    shop_address = models.CharField(max_length=200, blank=True)

@receiver(user_logged_in, sender=User)
def post_login(sender, user, request, **kwargs):
    client_ip, is_routable = get_client_ip(request)
    user.profile.ip_address = client_ip
    user.profile.save()