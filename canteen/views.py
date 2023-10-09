from django.shortcuts import render, redirect
from django.http import HttpResponse

from . models import *
from . forms import *
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem  # Import your FoodItem model or the relevant model
from django.contrib.auth.decorators import login_required

from django.db.models import Sum



def HomePage(request):

    food_items = FoodItem.objects.all()

    to_render = {
        'food_items': food_items
    }    
    return render(request, 'testHome.html', to_render)

def dashboardPage(request):
    return render(request, 'admin_dashboard.html', )

def add_to_cart(request, food_item_id):
    if request.method == 'POST' and request.user.is_authenticated:
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            food_item = get_object_or_404(FoodItem, pk=food_item_id)
            user = request.user

            # Get or create an order for the user
            order, created = Order.objects.get_or_create(user=user, is_paid=False)

            # Create or update the OrderItem
            try:
                order_item = OrderItem.objects.get(order=order, food_item=food_item)
                order_item.quantity += quantity
            except OrderItem.DoesNotExist:
                order_item = OrderItem(order=order, food_item=food_item, quantity=quantity)

            order_item.save()

            messages.success(request, 'Item added to your cart.')

            return redirect('canteen:home')
        else:
            # If form is not valid, show an error message
            messages.error(request, 'Invalid quantity.')
    
    # Handle cases where the user is not authenticated or it's not a POST request
    return redirect('canteen:home')

def update_cart_item(request, item_id):
    item = get_object_or_404(OrderItem, pk=item_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()

    return redirect('canteen:view_cart')

def delete_cart_item(request, item_id):
    item = get_object_or_404(OrderItem, pk=item_id)
    item.delete()
    return redirect('canteen:view_cart')

def view_cart(request):
    if request.user.is_authenticated:
        # Retrieve the user's cart items
        cart_items = OrderItem.objects.filter(order__user=request.user)
        
        # Calculate the total quantity and total price
        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_price = cart_items.aggregate(Sum('food_item__price'))['food_item__price__sum'] or 0

        context = {
            'cart_items': cart_items,
            'total_quantity': total_quantity,
            'total_price': total_price,
        }

        return render(request, 'view_cart.html', context)
    else:
        messages.error(request, 'You need to be logged in to view your cart.')
        return redirect('canteen:home')

def checkout(request):
    # Retrieve the user's cart items
    cart_items = OrderItem.objects.filter(order__user=request.user)

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'checkout.html', context)

# def payment(request):
#     if request.method == 'POST':
#         payment_type = request.POST.get('payment_type')
#         user = request.user

#         # Get the user's active order
#         order = Order.objects.get(user=user, is_paid=False)

#         # Calculate the total cost of the order by summing the costs of its associated OrderItem objects
#         total_cost = order.orderitem_set.aggregate(Sum('item_cost'))['item_cost__sum']

#         if total_cost is not None:
#             # Create a payment record
#             payment = Payment(order=order, payment_type=payment_type, amount_paid=total_cost)
#             payment.save()

#             # Mark the order as paid
#             order.is_paid = True
#             order.save()

#             return redirect('canteen:receipt')

#     return redirect('canteen:checkout')

# def receipt(request):
#     user = request.user
#     order = Order.objects.filter(user=user, is_paid=True).latest('id')
#     payment = Payment.objects.get(order=order)

#     context = {
#         'order': order,
#         'payment': payment,
#     }

#     return render(request, 'receipt.html', context)

def receipt(request):
    user = request.user
    order = Order.objects.filter(user=user, is_paid=True).latest('id')

    # Calculate the total quantity and total cost for this order
    total_quantity = order.orderitem_set.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_cost = order.orderitem_set.aggregate(Sum('food_item__price'))['food_item__price__sum'] or 0

    context = {
        'order': order,
        'total_quantity': total_quantity,
        'total_cost': total_cost,
    }

    return render(request, 'receipt.html', context)

# def payment(request):
#     if request.method == 'POST':
#         payment_type = request.POST.get('payment_type')
#         user = request.user

#         # Get the user's active order
#         order = Order.objects.get(user=user, is_paid=False)

#         # Initialize form variables
#         phone_number = None
#         account_number = None
#         expiring_date = None
#         pattern = None

#         if payment_type in ('Afri_Money', 'Orange_Money'):
#             phone_number = request.POST.get('phone_number')
#         elif payment_type == 'VISA Card':
#             account_number = request.POST.get('account_number')
#             expiring_date = request.POST.get('expiring_date')
#             pattern = request.POST.get('pattern')

#         # Calculate the total cost of the order by summing the costs of its associated OrderItem objects
#         total_cost = order.orderitem_set.annotate(
#             item_cost=ExpressionWrapper(F('food_item__price') * F('quantity'), output_field=DecimalField())
#         ).aggregate(Sum('item_cost'))['item_cost__sum']

#         if total_cost is not None:
#             # Create a payment record
#             payment = Payment(
#                 order=order,
#                 payment_type=payment_type,
#                 amount_paid=total_cost,
#                 phone_number=phone_number,
#                 account_number=account_number,
#                 expiring_date=expiring_date,
#                 pattern=pattern,
#             )
#             payment.save()

#             # Mark the order as paid
#             order.is_paid = True
#             order.save()

#             # Display a success message
#             messages.success(request, 'Payment successful!')

#             return redirect('canteen:receipt')
#         else:
#             # Display a failed message
#             messages.error(request, 'Payment failed. Please try again.')

#     return redirect('canteen:checkout')


# def payment(request):
#     if request.method == 'POST':
#         payment_type = request.POST.get('payment_type')
#         user = request.user

#         # Get the user's active order
#         order = Order.objects.get(user=user, is_paid=False)

#         # Calculate the total cost of the order by summing the costs of its associated OrderItem objects
#         total_cost = order.orderitem_set.aggregate(Sum('food_item__price'))['food_item__price__sum']

#         if total_cost is not None:
#             # Create a payment record
#             payment = Payment(order=order, payment_type=payment_type, amount_paid=total_cost)

#             if payment_type == 'MobileMoney':
#                 payment.phone_number = request.POST.get('phone_number')
#             elif payment_type == 'VisaCard':
#                 payment.account_number = request.POST.get('account_number')
#                 payment.expiring_date = request.POST.get('expiring_date')
#                 payment.pattern = request.POST.get('pattern')

#             payment.save()

#             # Mark the order as paid
#             order.is_paid = True
#             order.save()

#             return redirect('canteen:receipt')

#     return redirect('canteen:checkout')


def payment(request):
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        user = request.user

        # Get the user's active order
        order = Order.objects.get(user=user, is_paid=False)

        # Calculate the total cost of the order by summing the costs of its associated OrderItem objects
        total_cost = order.orderitem_set.aggregate(Sum('food_item__price'))['food_item__price__sum']

        if total_cost is not None:
            # Create a payment record
            payment = Payment(order=order, payment_type=payment_type, amount_paid=total_cost)

            if payment_type == 'MobileMoney':
                payment.phone_number = request.POST.get('phone_number')
            elif payment_type == 'VisaCard':
                payment.account_number = request.POST.get('account_number')
                payment.expiring_date = request.POST.get('expiring_date')
                payment.pattern = request.POST.get('pattern')

            payment.save()

            # Mark the order as paid
            order.is_paid = True
            order.save()

            # Add a success message for the user
            messages.success(request, 'Payment successful!')

            # Redirect to the receipt page or any other appropriate page
            return redirect('canteen:receipt')
        else:
            # Add an error message for the user
            messages.error(request, 'Payment failed. Please try again.')

    return redirect('canteen:checkout')