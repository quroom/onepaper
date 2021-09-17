from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from profiles.models import CustomUser


class Command(BaseCommand):
    help = "Closes the specified poll for voting"
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = getattr(
        settings, "ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS", 3
    )

    def handle(self, *args, **options):
        recent_unverified_joined_users = CustomUser.objects.filter(
            date_joined__lt=timezone.now()
            - timezone.timedelta(self.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS),
            emailaddress__verified=False,
        )
        if recent_unverified_joined_users.count():
            deleted_count = recent_unverified_joined_users.delete()
            print("cleanupregistration completed. Deleted user count=%d" % deleted_count[0])
        else:
            print("cleanupregistration completed. There is no user has to be deleted.")
