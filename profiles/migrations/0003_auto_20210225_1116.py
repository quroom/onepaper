# Generated by Django 3.1.5 on 2021-02-25 02:16

from django.db import migrations
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20210224_1418'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', profiles.models.CustomUserManager()),
            ],
        ),
    ]