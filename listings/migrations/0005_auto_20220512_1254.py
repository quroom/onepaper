# Generated by Django 3.1.5 on 2022-05-12 03:54

import django.db.models.deletion
import django_migration_linter as linter
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("listings", "0004_auto_20220420_1357"),
    ]

    operations = [
        linter.IgnoreMigration(),
        migrations.CreateModel(
            name="ListingItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("room_name", models.CharField(max_length=25)),
                ("bed", models.PositiveIntegerField(default=1)),
                ("security_deposit", models.PositiveBigIntegerField(blank=True, default=0)),
                ("monthly_fee", models.PositiveIntegerField(blank=True, default=0)),
                ("maintenance_fee", models.PositiveIntegerField(blank=True, default=0)),
                ("available_date", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="listing",
            name="short_lease",
        ),
        migrations.AddField(
            model_name="listing",
            name="available_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="ListingVisit",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("online_visit", models.BooleanField(default=True)),
                ("term_of_lease", models.SmallIntegerField(default=12)),
                ("visit_date", models.DateField(blank=True, null=True)),
                ("moving_date", models.DateField(blank=True, null=True)),
                ("content", models.TextField(blank=True)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="author_listingvisits",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="listing_visits",
                        to="listings.listing",
                    ),
                ),
                (
                    "listing_item",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="listing_item_visits",
                        to="listings.listingitem",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="listingitem",
            name="listing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="listings.listing"
            ),
        ),
    ]
