"""
Connect method docstring: Brief description of the connect method.
"""
from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser, PermissionsMixin

# Create your models here.


class CustomUserManager(UserManager):
    """
    Connect method docstring: Brief description of the connect method.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Connect method docstring: Brief description of the connect method.
        """
        if not email:
            raise ValueError("you have not provided a valid email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Connect method docstring: Brief description of the connect method.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_creator', False)
        extra_fields.setdefault('is_editor', False)
        extra_fields.setdefault('is_payment_verified', False)
        extra_fields.setdefault('is_pro', False)
        # extra_fields.setdefault('otp', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        Connect method docstring: Brief description of the connect method.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_creator', True)
        extra_fields.setdefault('is_editor', True)
        extra_fields.setdefault('is_payment_verified', True)
        extra_fields.setdefault('is_pro', True)
        # extra_fields.setdefault('otp', True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    """
    Connect method docstring: Brief description of the connect method.
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)

    is_editor = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_payment_verified = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=False)
    phone_number = models.CharField(unique=True, null=True, max_length=20)
    is_phone_active = models.BooleanField(default=False)
    # otp = models.IntegerField(default=0000, max_length=4)
    otp = models.CharField(max_length=4, default='',
                           null=True, blank=True, unique=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return self.email
