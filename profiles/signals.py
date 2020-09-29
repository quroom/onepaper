from profiles.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profile
from profiles.serializers import CustomUserSerializer

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
     if created:
         user = CustomUserSerializer(instance).data
         Profile.objects.create(user=instance, profile_name="Default")