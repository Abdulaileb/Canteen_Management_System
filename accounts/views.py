
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, AdminRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def admin_Dashboard(request):
    return render(request, 'admin/index.html')


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the student after registration
            messages.success(request, 'You have successfully created an account.')
            return redirect('canteen:home')  # Redirect to the student dashboard or desired page
        else:
            messages.error(request, 'Please enter your student email address')
    else:
        form = StudentRegistrationForm()
        
    
    return render(request, 'registration/register.html', {'form': form})

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_admin or user.is_superuser:
                print('success')
                return redirect('accounts:dashboard')  # Redirect to the admin dashboard
                
            elif user.is_student:
                return redirect('canteen:home')  # Redirect to the student dashboard
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'admin/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # Redirect to the login page after logout


from django.http import FileResponse

def create_income_chart(request):
    # This view is used to serve the income chart
    with open('income_chart.png', 'rb') as chart:
        return FileResponse(chart)
