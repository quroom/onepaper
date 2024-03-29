# Generated by Django 3.1.5 on 2021-09-17 04:37

from django.db import migrations, models
import django.db.models.deletion
import django_migration_linter as linter


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0004_createusersetting"),
    ]

    operations = [
        linter.IgnoreMigration(),
        migrations.CreateModel(
            name="Certification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("imp_uid", models.CharField(max_length=16)),
                ("ci", models.CharField(max_length=88)),
                ("di", models.CharField(max_length=66)),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="certification",
                        to="profiles.profile",
                    ),
                ),
            ],
        ),
    ]
