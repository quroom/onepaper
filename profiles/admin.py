from django.contrib import admin
from profiles.models import CustomUser, ExpertAuth, Profile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(ExpertAuth)