from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(default="profile.png")
    phone_number = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=50, null=True)
    ip_address = models.GenericIPAddressField(unpack_ipv4=True, null=True)