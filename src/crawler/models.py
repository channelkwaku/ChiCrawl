#from datetime import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class Bar(models.Model):
    name = models.CharField(max_length=60)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return self.name

class Address(models.Model):
    bar = models.ForeignKey('Bar')
    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(max_length=128)
    city = models.CharField(max_length=64, default="Chicago")
    state = models.CharField(max_length=30, default="Illinois")
    zip_code = models.CharField(max_length=5, default="60615")
    def __str__(self):
     return '{}, {}'.format(self.address_1, self.address_2)

