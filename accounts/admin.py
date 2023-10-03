from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from django.contrib.auth.forms import UserCreationForm

from .models import AdminUser, StudentUser
from django.contrib.auth.forms import UserCreationForm


# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):

#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['email', 'username', 'FUll_Name', 'is_staff', 'password1', 'password2' ] # new

# admin.site.register(CustomUser, CustomUserAdmin, CustomUserCreationForm)


# Customize the admin interface for AdminUser

class AdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AdminUser
        fields = ('username', 'email', 'full_name')

class AdminUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'full_name', 'is_active', 'is_staff', 'is_superuser')
    add_form = AdminUserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'username', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(AdminUser, AdminUserAdmin)

# Customize the admin interface for StudentUser
class StudentUserAdmin(UserAdmin):
    list_display = ('student_email', 'username', 'student_ID', 'department', 'levels', 'is_active')
    fieldsets = (
        (None, {'fields': ('student_email', 'username', 'student_ID', 'department', 'levels', 'password')}),
        ('Permissions', {'fields': ('is_active',)}),
    )

admin.site.register(StudentUser, StudentUserAdmin)
