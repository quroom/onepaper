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
    list_display = ("user", "updated_at", "get_name", "get_birthday", "address", "mobile_number")

    def get_name(self, obj):
        return obj.user.name

    get_name.admin_order_field = "profiles_customuser.name"  # Allows column order sorting
    get_name.short_description = "name"  # Renames column head

    def get_birthday(self, obj):
        return obj.user.birthday

    get_birthday.admin_order_field = "profiles_customuser.birthday"  # Allows column order sorting
    get_birthday.short_description = "birthday"  # Renames column head


admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
