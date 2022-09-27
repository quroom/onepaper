# Generated by Django 3.1.5 on 2022-09-27 02:02

import django_migration_linter as linter
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("addresses", "0003_address_detail"),
    ]

    operations = [
        linter.IgnoreMigration(),
        migrations.AlterField(
            model_name="address",
            name="bjdongName_eng",
            field=models.CharField(max_length=25),
        ),
    ]
