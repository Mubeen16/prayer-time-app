from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    timezone = models.CharField(max_length=50, default="UTC")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    REQUIRED_FIELDS = ['phone_number']
    
    def __str__(self):
        return f"{self.username} ({self.phone_number})"
