from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Student Email field must be set')
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['role'] = CustomUser.ADMIN  # Set the role to "admin"
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    USERS = 'users'
    ADMIN = 'admin'
    MANAGER = 'manager'

    ROLE_CHOICES = [
        (USERS, _('Users')),
        (ADMIN, _('Admin')),
        (MANAGER, _('Manager')),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USERS)
    contacts = models.CharField(max_length=10, blank=True, null=True)
    is_staff = models.BooleanField(default=False)  # Admin users are staff
    full_name = models.CharField(max_length=100)

    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def is_users(self):
        return self.role == self.USERS

    @property
    def is_admin(self):
        return self.role == self.ADMIN
    
    @property
    def is_manager(self):
        return self.role == self.MANAGER

    def save(self, *args, **kwargs):
        if self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)




