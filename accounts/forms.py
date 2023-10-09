# from django import forms
# # from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# from django.contrib.auth import get_user_model


# # class CustomAdminCreationForm(UserCreationForm):
# #     class Meta(UserCreationForm.Meta):
# #         model = CustomUser
# #         fields = ['email', 'username', 'Full_Name', 'password1', 'password2']

# # class CustomAdminChangeForm(UserChangeForm):
# #     class Meta:
# #         model = CustomUser
# #         fields = UserChangeForm.Meta.fields

# # class CustomUserCreationForm(UserCreationForm):
# #     class Meta:
# #         model = get_user_model()
# #         fields = ['username', 'student_ID', 'department', 'levels', 'student_email', 'password1', 'password2']

# # class CustomUserChangeForm(UserChangeForm):
# #     class Meta:
# #         model = get_user_model()
# #         fields = UserChangeForm.Meta.fields

# from django import forms
# from .models import AdminUser, StudentUser
# from django.contrib.auth.forms import AuthenticationForm

# class AdminUserRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = AdminUser
#         fields = ['username', 'email', 'full_name', 'password']

# class StudentUserRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = StudentUser
#         fields = ['username', 'student_ID', 'department', 'levels', 'student_email', 'password']

# class CustomLoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


from django import forms
from .models import CustomUser

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'student_ID', 'department', 'levels', 'email', 'full_name']

    def save(self, commit=True):
        # Get the user instance from the form
        user = super().save(commit=False)

        # Hash the password using set_password
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user

        


class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'full_name']
