# Generated by Django 3.1.5 on 2022-02-06 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20211015_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='expertprofile',
            name='is_shown_ho',
            field=models.BooleanField(default=True, null=True),
        ),
    ]