# Generated by Django 3.1.5 on 2022-02-09 04:44

import django.db.models.deletion
from django.db import migrations, models


def set_defaultstatus(apps, schema_editor):
    Listing = apps.get_model("listings", "Listing")
    ListingStatus = apps.get_model("listings", "ListingStatus")
    for listing in Listing.objects.all():
        if not hasattr(listing, "listingstatus"):
            ListingStatus.objects.create(listing=listing)


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ListingStatus",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("status", models.SmallIntegerField(choices=[(0, "만실"), (1, "가능")], default=1)),
                (
                    "listing",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="listings.listing"
                    ),
                ),
            ],
        ),
        migrations.RunPython(set_defaultstatus),
    ]