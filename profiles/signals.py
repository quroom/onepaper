from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from profiles.models import Profile, AllowedUser
from profiles.serializers import CustomUserSerializer

@receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
     if created:
         allowedUser = AllowedUser.objects.create(profile=instance)

@receiver(post_delete, sender=Profile)
def delete_address(sender, instance, **kwargs):
    if not instance.address is None:
        instance.address.delete()