from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    puesto = models.CharField(max_length=100, null=True, blank=True)
    rango = models.IntegerField(null=True, blank=True)
    edad = models.CharField(max_length=3, null=True, blank=True)
    antiguedad = models.CharField(max_length=3 ,null=True, blank=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []