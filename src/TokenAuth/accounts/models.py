from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.db import models


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    liked = models.ManyToManyField('Post', blank=True, related_name='users')


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=None)
    rating = models.IntegerField(default=0)
    status = models.CharField(default='', max_length=127, blank=True, null=True)
    description = models.CharField(default='', max_length=511, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='/default/default.jpg')


class Post(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    article = models.CharField(default='', max_length=255)
    text = models.CharField(default='', max_length=4095)
    likes = models.IntegerField(default=0)

    def add_like(self):
        self.likes += 1

    def remove_like(self):
        self.likes -= 1


class PostImage(models.Model):
    image = models.ImageField(upload_to='posts/')
    position = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
