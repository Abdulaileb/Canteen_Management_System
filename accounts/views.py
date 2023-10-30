
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, AdminRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from accounts .forms import *


def Dashboard(request):

    items = CartItemAdded.objects.all()

    context = {'items':items}

    return render(request, 'dashboard/index.html', context)


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the student after registration
            #messages.success(request, 'You have successfully created an account.')

            messages.success(request, 'Success message', extra_tags='success')
            return redirect('canteen:home')  # Redirect to the student dashboard or desired page
        else:
            messages.error(request, 'Please enter your student email address')
    else:
        form = StudentRegistrationForm()
        
    
    return render(request, 'registration/register.html', {'form': form})

def register_admin(request):

    admin_users = CustomUser.objects.filter(role=CustomUser.ADMIN)

    # Check if the current user is a superuser before allowing admin registration
    # if not request.user.is_superuser:
    #     return redirect('accounts:login')  # Redirect to login or an unauthorized page

    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create user instance without saving to the database
            user.role = CustomUser.ADMIN  # Set the role to "admin" (employee)
            user.save()  # Now save the user to the database
            # form.save()
            messages.success(request, 'Admin user created successfully')
            return redirect('accounts:manage-employees')  # Redirect to the admin dashboard or desired page
    else:
        form = AdminRegistrationForm()

    context = {'admin_users':admin_users,
               'form': form,
               }
    
    return render(request, 'dashboard/users/manage_employees.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_admin or user.is_superuser:
                print('success')
                return redirect('admin:index')  # Redirect to the admin dashboard
            
            elif user.is_cashier:
                return redirect('accounts:dashboard')
                
            elif user.is_student:
                return redirect('canteen:home')  # Redirect to the student dashboard
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # Redirect to the login page after logout


from django.http import FileResponse

def create_income_chart(request):
    # This view is used to serve the income chart
    with open('income_chart.png', 'rb') as chart:
        return FileResponse(chart)





####### USER FOOD ITEMS ########

def manage_food_category(request):

    foodCategory = FoodCategory.objects.all()

    form = FoodCategoryForm()
    if request.method == 'POST':
        form = FoodCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food Category has been successfully added')
            return redirect('accounts:manage_foodCategory')
    else:
            # messages.error(request, 'Check the fields again')
        form = FoodCategoryForm()
    context = {'form':form,
               'foodCategory':foodCategory,
               }

    return render(request, 'dashboard/manage-food/food-category.html', context)

def manage_food_items(request):

    foodItems = FoodItem.objects.all()

    form = FoodItemsForm()
    if request.method == 'POST':
        form = FoodItemsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food Items has been successfully added')
            return redirect('accounts:manage_foodItems')
    else:
            # messages.error(request, 'Check the fields again')
        form = FoodItemsForm()
    context = {'form':form,
               'foodItems':foodItems,
               }

    return render(request, 'dashboard/manage-food/food-items.html', context)

def OrderListView(request):
    items = CartItemAdded.objects.all()
    context = {'items':items}
    return render(request, 'dashboard/orders/manage_orders.html', context)



def user_list(request):
    student_users = CustomUser.objects.filter(role=CustomUser.STUDENT)

    context = {'student_users':student_users}
    
    return render(request, 'dashboard/users/manage_students.html', context)

# def admin_list(request):
    
#     admin_users = CustomUser.objects.filter(role=CustomUser.ADMIN)

#     context = {'admin_users':admin_users}
    
#     return render(request, 'admin/users/manage_employees.html', context)

def summary_report(request):
    # Get all order items to create the summary report
    order_items = OrderItem.objects.all()

    context = {
        'order_items': order_items,
    }

    return render(request, 'admin/report/report.html', context)



def management_report(request):
    # Filter users who have placed orders
    users_with_orders = CustomUser.objects.filter(order__isnull=False).distinct()

    # Gather data for the report based on the filtered users
    orders = Order.objects.filter(user__in=users_with_orders)
    payments = Payment.objects.filter(order__in=orders)
    receipts = Receipt.objects.filter(order__in=orders)

    # Calculate relevant statistics or perform any data manipulation as needed

    context = {
        'orders': orders,
        'payments': payments,
        'receipts': receipts,
    }

    return render(request, 'dashboard/report/report.html', context)



def view_receipts(request):
    total_receipts = Receipt.objects.all()

    context = {
        'total_receipts':total_receipts
    }

    return render(request, 'dashboard/report/report.html', context)