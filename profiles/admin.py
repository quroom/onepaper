from django.contrib import admin
from profiles.models import CustomUser, Profile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)