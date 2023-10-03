from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth import get_user_model


# class CustomAdminCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ['email', 'username', 'Full_Name', 'password1', 'password2']

# class CustomAdminChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = UserChangeForm.Meta.fields

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'student_ID', 'department', 'levels', 'student_email', 'password1', 'password2']

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = get_user_model()
#         fields = UserChangeForm.Meta.fields

from django import forms
from .models import AdminUser, StudentUser

class AdminUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ['username', 'email', 'full_name', 'password']

class StudentUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = StudentUser
        fields = ['username', 'student_ID', 'department', 'levels', 'student_email', 'password']
