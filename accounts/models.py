from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import BaseUserManager


# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, student_ID, department, levels, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, student_ID=student_ID, department=department, levels=levels, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, student_ID, department, levels, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(username, email, student_ID, department, levels, password, **extra_fields)

# class CustomUser(AbstractUser):
#     student_ID = models.CharField(max_length=10, unique=True)
#     department = models.CharField(max_length=50)
#     levels = models.CharField(max_length=10)
#     student_email = models.EmailField(unique=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'student_email'
#     REQUIRED_FIELDS = ['username', 'student_ID', 'department', 'levels']


# # Common fields for both regular users and admin users
# class UserProfile(models.Model):
#     user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE)
#     # Add common fields here
#     full_name = models.CharField(max_length=100)
#     # Other common fields

#     def __str__(self):
#         return self.user.username

# # Custom user model for regular users (students)
# class CustomUser(AbstractUser):
#     student_ID = models.CharField(max_length=10, unique=True)
#     department = models.CharField(max_length=50)
#     levels = models.CharField(max_length=10)
#     student_email = models.EmailField(unique=True)
#     # Other fields specific to regular users

#     def __str__(self):
#         return self.username

# # Custom user model for admin users
# class AdminUser(models.Model):
#     user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE)
#     is_admin = models.BooleanField(default=False)
#     is_super_user = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     # Other fields specific to admin users

#     def __str__(self):
#         return self.user.username

class AdminUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, blank=True, related_name='admin_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='admin_users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email
    

class StudentUser(AbstractUser):
    student_ID = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=50)
    levels = models.CharField(max_length=10)
    student_email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='student_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='student_users')

    USERNAME_FIELD = 'student_email'

    def __str__(self):
        return self.student_email

