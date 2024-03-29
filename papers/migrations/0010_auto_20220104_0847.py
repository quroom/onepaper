# Generated by Django 3.1.5 on 2022-01-03 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0009_auto_20210906_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifyingexplanation',
            name='floor_surface_status',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='verifyingexplanation',
            name='floor_surface_status_info',
            field=models.CharField(blank=True, max_length=22, null=True),
        ),
        migrations.AddField(
            model_name='verifyingexplanation',
            name='multi_family_housing_document',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
