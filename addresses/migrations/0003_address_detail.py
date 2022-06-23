# Generated by Django 3.1.5 on 2022-06-22 03:00

from django.db import migrations, models, transaction


@transaction.atomic
def make_detail_address(apps, schema_editor):
    Address = apps.get_model("addresses", "Address")

    for address in Address.objects.all():
        is_updated = False
        if address.dong != "" and address.dong != None:
            if address.dong[-1] != "동":
                address.detail = address.dong + "동"
            else:
                address.detail = address.dong
            is_updated = True
        if address.ho != "" and address.ho != None:
            ho = address.ho
            if is_updated:
                address.detail += " "
            else:
                address.detail = ""
            if ho[-1] != "호" and ho[-1] != "층":
                address.detail += ho + "호"
            else:
                address.detail += ho
            is_updated = True
        address.save()


class Migration(migrations.Migration):

    dependencies = [
        ("addresses", "0002_dong"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="detail",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.RunPython(code=make_detail_address, reverse_code=migrations.RunPython.noop),
    ]
