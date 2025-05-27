from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    language = models.CharField(max_length=20, default='en')
    manager = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email']