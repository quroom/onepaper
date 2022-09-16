from django.apps import apps
from django.contrib import admin

from papers.models import Contractor

# Register your models here.
for model in apps.get_app_config("papers").get_models():
    if model != Contractor:
        admin.site.register(model)


class ContractorAdmin(admin.ModelAdmin):
    list_display = ("updated_at", "profile")


admin.site.register(Contractor, ContractorAdmin)
