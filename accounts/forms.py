from django import forms
from .models import CustomUser

from canteen.models import *

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'student_ID', 'department', 'levels', 'email', 'full_name']

    email = forms.EmailField(
        error_messages={
            'invalid': 'Invalid email. Enter your student email ending with @cusl.com.',
        }
    )

    def clean_email(self):
        email = self.cleaned_data['email']

        # Check if the email ends with "cusl.com"
        if not email.endswith('@cusl.com'):
            raise forms.ValidationError("Email must end with @cusl.com")

        return email

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user




class FoodCategoryForm(forms.ModelForm):
    class Meta:
        model = FoodCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
       


class FoodItemsForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

