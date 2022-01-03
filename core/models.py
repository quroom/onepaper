from django.conf import settings
from django.db import models


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    content = models.TextField()

    class Meta:
        abstract = True
