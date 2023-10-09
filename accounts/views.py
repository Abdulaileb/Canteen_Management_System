# from django.shortcuts import render, redirect
# # from django.contrib.auth.forms import UserCreationForm
# # from django.urls import reverse_lazy
# # from django.views import generic
# # from . forms import CustomUserCreationForm

# from django.contrib.auth import login, authenticate, logout
# from .forms import AdminUserRegistrationForm, StudentUserRegistrationForm

# from django.contrib import messages

# from . models import *
# import logging


# logger = logging.getLogger(__name__)

# # class SignUpView(generic.CreateView):

# #     form_class = CustomUserCreationForm
# #     success_url = reverse_lazy('login')
# #     template_name = 'registration/sign_up.html'

# # def user_creation_form(request):
# #     if request.method == 'POST':
# #         form = CustomUserCreationForm(request.POST)
# #         if form.is_valid():
# #             user = form.save()
# #             return redirect('dashboard')
# #     else:
# #         form = CustomUserCreationForm()
# #     return render(request, 'registration/sign_up.html', {'form': form})

# def admin_user_registration(request):
#     if request.method == 'POST':
#         form = AdminUserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('admin:index')  # Redirect to admin dashboard or any other page
#     else:
#         form = AdminUserRegistrationForm()
#     return render(request, 'registration/admin_user_registration.html', {'form': form})

# def student_user_registration(request):
#     if request.method == 'POST':
#         form = StudentUserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')  # Redirect to student dashboard or any other page
#     else:
#         form = StudentUserRegistrationForm()
#     return render(request, 'registration/student_user_registration.html', {'form': form})

# # def loginPage(request):
# #     if request.method == 'POST':
# #         username = request.POST.get('username')
# #         password = request.POST.get('password')

# #         admin_user = authenticate(request, username=username, password=password)
# #         student_user = StudentUser.objects.filter(username=username).first()

# #         if admin_user is not None:
# #             # If the user is an admin, log them in and redirect to the admin dashboard
# #             login(request, admin_user)
# #             if admin_user.is_superuser or admin_user.groups.filter(name='admin').exists():
# #                 return redirect('admin:index')

# #         elif student_user is not None:
# #             # If the user is a student, log them in and redirect to the student dashboard
# #             user = authenticate(request, username=student_user.username, password=password)
# #             if user is not None:
# #                 login(request, user)
# #                 return redirect('home')  # Replace 'student_dashboard' with your student dashboard URL
# #         else:
# #             messages.error(request, 'Invalid username or password')

# #     return render(request, 'registration/login.html')

# def loginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         logger.debug(f"Login attempt with username: {username} and password: {password}")

#         try:
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 if user.is_superuser or user.groups.filter(name='admin').exists():
#                     return redirect('admin:index')
#                 else:
#                     return redirect('home')
#             else:
#                 messages.error(request, 'Invalid username or password')
#                 print('MEET ME HERE')
#         except Exception as e:
#             messages.error(request, f'An error occurred: {str(e)}')

#     return render(request, 'registration/login.html')

# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
# from .forms import *

# # def student_user_registration(request):
# #     if request.method == 'POST':
# #         form = StudentUserRegistrationForm(request.POST)
# #         if form.is_valid():
# #             user = form.save()
# #             login(request, user)
# #             return redirect('home')  # Redirect to student dashboard or any other page
# #     else:
# #         form = StudentUserRegistrationForm()
    
# #     # Check if the request contains a 'login' parameter
# #     if 'login' in request.GET:
# #         login_form = CustomLoginForm(request.POST)
# #         if login_form.is_valid():
# #             username = login_form.cleaned_data['username']
# #             password = login_form.cleaned_data['password']
# #             user = authenticate(request, username=username, password=password)
# #             if user is not None:
# #                 login(request, user)
# #                 if user.is_superuser or user.groups.filter(name='admin').exists():
# #                     return redirect('admin:index')
# #                 else:
# #                     return redirect('home')
# #             else:
# #                 messages.error(request, 'Invalid username or password')

# #     return render(request, 'registration/student_user_registration.html', {'form': form})


from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, AdminRegistrationForm
from django.contrib import messages

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the student after registration
            return redirect('home')  # Redirect to the student dashboard or desired page
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'registration/register_student.html', {'form': form})

def register_admin(request):
    # Check if the current user is a superuser before allowing admin registration
    if not request.user.is_superuser:
        return redirect('login')  # Redirect to login or an unauthorized page

    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin user created successfully')
            return redirect('admin_dashboard')  # Redirect to the admin dashboard or desired page
    else:
        form = AdminRegistrationForm()
    
    return render(request, 'registration/register_admin.html', {'form': form})


from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import render, redirect
# from .forms import RegistrationForm
# from django.contrib import messages

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Automatically log in the user after registration
#             login(request, user)
#             return redirect('dashboard')  # Redirect to the dashboard or desired page
#     else:
#         form = RegistrationForm()
    
#     return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('admin_dashboard')  # Redirect to the admin dashboard
            elif user.is_student:
                return redirect('canteen:home')  # Redirect to the student dashboard
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


from django.http import FileResponse

def create_income_chart(request):
    # This view is used to serve the income chart
    with open('income_chart.png', 'rb') as chart:
        return FileResponse(chart)
