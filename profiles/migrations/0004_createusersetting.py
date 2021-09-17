import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def create_usersetting(apps, schema_editor):
    CustomUser = apps.get_model("profiles", "CustomUser")
    UserSetting = apps.get_model("profiles", "UserSetting")
    for user in CustomUser.objects.all():
        UserSetting.objects.create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0003_usersetting"),
    ]

    operations = [migrations.RunPython(create_usersetting)]
