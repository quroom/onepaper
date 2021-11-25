# Generated by Django 3.1.5 on 2021-10-15 03:19

import django_migration_linter as linter
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20211014_1008'),
    ]

    operations = [
        linter.IgnoreMigration(),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-is_activated', '-updated_at']},
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='is_default',
            new_name='is_activated',
        ),
    ]
