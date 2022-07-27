from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None):
        from .models import Profile
        user_profile = Profile.objects.create()
        user = self.model(
                username=username,
                profile=user_profile,
                )

        if not password:
            password = ''.join([chr(i) for i in range(100, 120)])
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, email=None):
        user = self.create_user(username, password, email)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
