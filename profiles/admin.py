from django.apps import apps
from django.contrib import admin

from profiles.models import CustomUser, Profile

# Register your models here.
for model in apps.get_app_config("profiles").get_models():
    if model != Profile and model != CustomUser:
        admin.site.register(model)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "updated_at", "name", "birthday")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "updated_at", "address", "mobile_number")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
