from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

## To display everything tot he admin user 
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'contacts', 'full_name', 'is_staff')
    list_filter = ('role', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'full_name')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'full_name', 'is_staff'),
        }),
    )
    search_fields = ('username', 'email', 'contacts', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
