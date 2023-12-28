from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from uuid import uuid4
import os

class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateTimeField(null=True)
    profile_picture = models.ImageField(default="default.png", upload_to='profile_pics')
    phone_number = models.BigIntegerField(null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=50, null=True)
    ip_address = models.GenericIPAddressField(unpack_ipv4=True, null=True)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"users_{User.objects.count() + 1}"
        super().save(*args, **kwargs)
        
        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)