from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views import generic
# from . forms import CustomUserCreationForm

from django.contrib.auth import login
from .forms import AdminUserRegistrationForm, StudentUserRegistrationForm

# class SignUpView(generic.CreateView):

#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/sign_up.html'

# def user_creation_form(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             return redirect('dashboard')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/sign_up.html', {'form': form})

def admin_user_registration(request):
    if request.method == 'POST':
        form = AdminUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('admin:index')  # Redirect to admin dashboard or any other page
    else:
        form = AdminUserRegistrationForm()
    return render(request, 'registration/admin_user_registration.html', {'form': form})

def student_user_registration(request):
    if request.method == 'POST':
        form = StudentUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_dashboard')  # Redirect to student dashboard or any other page
    else:
        form = StudentUserRegistrationForm()
    return render(request, 'registration/student_user_registration.html', {'form': form})
