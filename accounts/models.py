from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings



class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None):
        user = self.create_user(email, phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=100, blank=True, null=True)   # ✅ Added
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)  # ✅ Added for creation date


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email

# User = settings.AUTH_USER_MODEL  # agar custom user use kar rahe ho

class LoggedInUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)  # True jab user login ho
    session_key = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"{self.user} ({'online' if self.is_active else 'offline'})"
