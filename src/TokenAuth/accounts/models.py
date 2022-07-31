from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.db import models


class Post(models.Model):
    article = models.CharField(default='', max_length=255)
    text = models.CharField(default='', max_length=4095)


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    posts = models.ForeignKey(Post, on_delete=models.PROTECT)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=None)
    rating = models.IntegerField(default=0)
    status = models.CharField(default='', max_length=127, blank=True, null=True)
    description = models.CharField(default='', max_length=511, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='/default/default.jpg')
