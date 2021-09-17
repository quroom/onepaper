from django.apps import apps
from django.contrib import admin

# Register your models here.
for model in apps.get_app_config("profiles").get_models():
    admin.site.register(model)
