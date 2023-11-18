
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsersRegistrationForm, AdminRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from accounts .forms import *

from canteen.models import * 


def Dashboard(request):

    items = Order.objects.all()

    total_user_count = CustomUser.objects.filter(role=CustomUser.USERS).count()

    food_category = FoodCategory.objects.count()

    items_available = InventoryItem.objects.count()

    food_items = FoodItem.objects.count()

    items_ordered = Order.objects.count()

    total_reports = Receipt.objects.count()

    total_inventory = InventoryItem.objects.count()


    orders = Order.objects.all().order_by('-order_date')
   
    accumulated_amount = 0  # Initialize the accumulated amount

    for order in orders:
        total_cost = sum(item.quantity * item.food_item.price for item in order.orderitem_set.all())
        accumulated_amount += total_cost  # Add to the accumulated amount
       

    context = {'items':items,
               'total_user_count':total_user_count,
               'food_category':food_category,
               'items_ordered':items_ordered,
               'food_items':food_items,
               'items_available':items_available,
               'total_reports':total_reports,
               'total_inventory':total_inventory,
               'accumulated_amount':accumulated_amount
               }

    return render(request, 'dashboard/index.html', context)


def register_user(request):

    if request.method == 'POST':

        form = UsersRegistrationForm(request.POST)

        if form.is_valid():

            print (form)

            user = form.save()

            

            login(request, user)  # Automatically log in the user after registration
            #messages.success(request, 'You have successfully created an account.')

            messages.success(request, 'Success message', extra_tags='success')
            return redirect('canteen:home')  # Redirect to the student dashboard or desired page
        else:
            messages.error(request, 'OOps! An error ocurred, Please check your form and try again')
    else:
        form = UsersRegistrationForm()
        
    
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
            
            elif user.is_manager:
                return redirect('accounts:dashboard')
                
            elif user.is_users:
                return redirect('canteen:home')  # Redirect to the student dashboard
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('canteen:index_unauthenticated')  # Redirect to the login page after logout


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


def manage_inventory_category(request):

    inventory = InventoryItem.objects.all()

    form = InventoryForm()
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory has been successfully added')
            return redirect('accounts:manage-inventory')
    else:
            # messages.error(request, 'Check the fields again')
        form = InventoryForm()
    context = {'form':form,
               'inventory':inventory,
               }

    return render(request, 'dashboard/manage-inventory/manage-inventory.html', context)




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
    items = Order.objects.all()
    context = {'items':items}
    return render(request, 'dashboard/orders/manage_orders.html', context)



def user_list(request):
    users = CustomUser.objects.filter(role=CustomUser.USERS)

    if request.method == 'POST':
        form = UsersRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Add any additional logic you need after creating the user
            messages.success(request, 'User created successfully', extra_tags='success')
            return redirect('accounts:manage-users')
        else:
            messages.error(request, 'Please enter valid information')

    else:
        form = UsersRegistrationForm()


    context = {'users':users,
               'form':form,
               }
    
    return render(request, 'dashboard/users/manage_users.html', context)

# def update_user(request, user_id):
#     user = CustomUser.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UsersRegistrationForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'User updated successfully', extra_tags='success')
#             return redirect('accounts:manage-users')
#     else:
#         form = UsersRegistrationForm(instance=user)

#     context = {'form': form}
#     return render(request, 'dashboard/users/update_user.html', context)

def update_users(request, user_id):

    # Try to get the user with the specified ID and role 'users'
    user = get_object_or_404(CustomUser, id=user_id, role=CustomUser.USERS)

    print("Updating user:", user, "with role:", user.role)  # Debug print

    # Check if the user has the 'users' role
    # if user.role != CustomUser.USERS:
    #     messages.error(request, "You can only update users with 'users' role.")
    #     return redirect('accounts:manage-users')
    
    if request.method == 'POST':
        form = UsersUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully', extra_tags='success')
            return redirect('accounts:manage-users')
    else:
        form = UsersUpdateForm(instance=user)

    context = {'form': form}
    # Note: This template should only contain the form and necessary form fields
    return render(request, 'dashboard/users/update_user.html', context)


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



# def view_receipts(request):
#     total_receipts = Receipt.objects.all()

#     context = {
#         'total_receipts':total_receipts
#     }

#     return render(request, 'dashboard/report/report.html', context)

from datetime import datetime

def all_receipts(request):
    # Retrieve all orders
    orders = Order.objects.all().order_by('-order_date')
    receipts = []
    accumulated_amount = 0  # Initialize the accumulated amount

    for order in orders:
        total_cost = sum(item.quantity * item.food_item.price for item in order.orderitem_set.all())
        accumulated_amount += total_cost  # Add to the accumulated amount
        receipts.append({
            'order_id': order.id,
            'user': order.user.username,
            'amount': total_cost,
            'date': order.order_date.strftime('%Y-%m-%d')
        })

    return render(request, 'dashboard/receipt/receipt.html', {'receipts': receipts, 'accumulated_amount': accumulated_amount })
