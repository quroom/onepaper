from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profile, AuthedUser
from profiles.serializers import CustomUserSerializer

@receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
     if created:
         AuthedUser.objects.create(profile=instance)