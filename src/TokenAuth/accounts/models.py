from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    objects = CustomUserManager()
