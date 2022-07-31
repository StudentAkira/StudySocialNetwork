from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from accounts.models import CustomUser, Profile, Post, PostImage


class CustomUserAdmin(admin.ModelAdmin):
    fields = [('username', 'password')]


admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostImage)
