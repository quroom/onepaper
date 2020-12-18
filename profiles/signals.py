from django.db.models.signals import post_delete
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from ipware import get_client_ip
from profiles.models import AllowedUser, CustomUser, Profile
from profiles.serializers import CustomUserSerializer

@receiver(post_delete, sender=Profile)
def delete_address(sender, instance, **kwargs):
    if not instance.address is None:
        instance.address.delete()

@receiver(user_logged_in, sender=CustomUser)
def post_login(sender, user, request, **kwargs):
    client_ip, is_routable = get_client_ip(request)
    user.ip_address = client_ip
    user.save()