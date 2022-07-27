from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.db import models
from TokenAuth.settings import MEDIA_URL


class Profile(models.Model):
    rating = models.IntegerField(default=0)
    status = models.CharField(default='', max_length=127, blank=True, null=True)
    description = models.CharField(default='', max_length=511, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='media/default/default.jpg')


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, default=None)
