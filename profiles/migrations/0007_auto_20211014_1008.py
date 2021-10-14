# Generated by Django 3.1.5 on 2021-10-14 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_createcertification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='ci',
            field=models.CharField(blank=True, max_length=88),
        ),
        migrations.AlterField(
            model_name='certification',
            name='di',
            field=models.CharField(blank=True, max_length=66),
        ),
        migrations.AlterField(
            model_name='certification',
            name='imp_uid',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='certification',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
