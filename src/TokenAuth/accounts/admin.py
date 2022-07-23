from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from accounts.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    fields = [('username', 'password')]


admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)
