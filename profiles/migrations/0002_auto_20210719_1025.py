# Generated by Django 3.1.5 on 2021-07-19 01:25

from django.db import migrations
import django_migration_linter as linter


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        linter.IgnoreMigration(),
        migrations.AlterModelOptions(
            name="customuser",
            options={"ordering": ["-last_login"]},
        ),
    ]
