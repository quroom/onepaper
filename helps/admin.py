from django.contrib import admin
from django.db import models
from django_summernote.admin import SummernoteModelAdmin

from helps.models import Notice


class NoticeAdmin(SummernoteModelAdmin):
    summernote_fields = "__all__"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            # setting the user from the request object
            kwargs["initial"] = request.user.id
            # making the field readonly
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Notice, NoticeAdmin)
