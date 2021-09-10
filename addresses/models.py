from django.db import models


# Create your models here.
class Address(models.Model):
    old_address = models.CharField(max_length=250)
    old_address_eng = models.CharField(max_length=250)
    new_address = models.CharField(max_length=250)
    bjdongName = models.CharField(max_length=20)
    bjdongName_eng = models.CharField(max_length=20)
    sigunguCd = models.CharField(max_length=5)
    bjdongCd = models.CharField(max_length=5)
    platGbCd = models.CharField(max_length=1, blank=True)
    bun = models.CharField(max_length=4, blank=True)
    ji = models.CharField(max_length=4, blank=True)
    dong = models.CharField(max_length=20, blank=True)
    ho = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.old_address)
