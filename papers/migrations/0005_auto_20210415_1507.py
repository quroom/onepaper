# Generated by Django 3.1.5 on 2021-04-15 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0004_auto_20210415_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='noise_status',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='sunshine_status',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='vibration',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='wall_paper_status',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
