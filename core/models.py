from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserRole(models.TextChoices):
    CUSTOMER = 'CUSTOMER', 'Customer'
    STAFF = 'STAFF', 'Staff (Maker)'
    ADMIN = 'ADMIN', 'Admin (Checker)'


class UserManager(BaseUserManager):

    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required.')
        if not phone:
            raise ValueError('Phone number is required.')

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('role', UserRole.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'full_name']

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.full_name} ({self.role})'
