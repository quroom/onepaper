from django.db.models.signals import post_delete, post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from ipware import get_client_ip
from profiles.models import AllowedUser, CustomUser, ExpertProfile, Profile
from profiles.serializers import CustomUserSerializer

@receiver(post_save, sender=ExpertProfile)
def post_expert_profile(sender, instance, **kwargs):
    if instance.status != ExpertProfile.REQUEST:
        instance.status = ExpertProfile.REQUEST
        instance.save()

@receiver(post_delete, sender=Profile)
def delete_address(sender, instance, **kwargs):
    if not instance.address is None:
        instance.address.delete()

@receiver(user_logged_in, sender=CustomUser)
def post_login(sender, user, request, **kwargs):
    client_ip, is_routable = get_client_ip(request)
    user.ip_address = client_ip
    user.save()