from django.db import models
from django.conf import settings

# Create your models here.
class Notice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title
    
class Manual(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='childrens', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)

    def __str__(self):
        if self.parent is None:
            return self.title
        else:
            return str(self.parent)+'-'+self.title
