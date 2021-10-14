import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def create_usersetting(apps, schema_editor):
    Profile = apps.get_model("profiles", "Profile")
    Certification = apps.get_model("profiles", "Certification")
    for profile in Profile.objects.all():
        if not hasattr(profile, "certification"):
            Certification.objects.create(profile=profile)


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0005_certification"),
    ]

    operations = [migrations.RunPython(create_usersetting)]
