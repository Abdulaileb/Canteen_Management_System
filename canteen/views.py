from django.shortcuts import render, redirect
from django.http import HttpResponse

from . models import *
from . forms import *
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem  # Import your FoodItem model or the relevant model
from django.contrib.auth.decorators import login_required

from django.db.models import Sum, F
from django.core.exceptions import ObjectDoesNotExist

# from django.http import HttpResponse
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet

from . decorators import user_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import redirect
from django.db import transaction

import io
from reportlab.pdfgen import canvas

from datetime import datetime

# View for unauthenticated users
def index_for_unauthenticated(request):

    context = get_common_context()

    top_items = FoodItem.objects.all()[:3]

    if request.user.is_authenticated:
        # Redirect authenticated users to the authenticated index view
        return HomePage(request)
    else:
        # Render the template for unauthenticated users

        obj = {
            'context':context,
            'top_items': top_items
        }
        return render(request, 'public/index.html', obj)

@login_required
def HomePage(request):

    food_items = FoodItem.objects.all()

    top_items = FoodItem.objects.all()[:3]

    context = get_common_context()

   

    to_render = {
        'food_items': food_items,
        'top_items':top_items,
        'context':context,
        # 'user': user, 'orders': orders, 'payments': payments, 'receipts': receipts
    }    
    return render(request, 'index.html', to_render)

def get_common_context():
    food_items = FoodItem.objects.all()
    categories = FoodCategory.objects.all().prefetch_related('fooditem_set')
    return {
        'food_items': food_items,
        'categories': categories
    }

def aboutUs(request):
    return render(request, 'public/about.html')

def contactUs(request):
    return render(request, 'public/contact.html')

def Products(request):

    context = get_common_context()

    food_items = context['food_items']  # Extract food_items from the context


    paginator = Paginator(food_items, 10) # Show 10 food items per page

    page = request.GET.get('page')

    try:
        food_items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        food_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        food_items = paginator.page(paginator.num_pages)
   
    return render(request, 'public/product.html', context)

def Product(request):

    context = get_common_context()

    food_items = context['food_items']  # Extract food_items from the context


    paginator = Paginator(food_items, 10) # Show 10 food items per page

    page = request.GET.get('page')

    try:
        food_items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        food_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        food_items = paginator.page(paginator.num_pages)
   
    return render(request, 'product.html', context)

def Contact(request):
    return render(request, 'contact.html',)

def dashboardPage(request):
    return render(request, 'admin_dashboard.html', )

@user_required
def add_to_cart(request, food_item_id):
    if request.method == 'POST' and request.user.is_authenticated:
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            food_item = get_object_or_404(FoodItem, pk=food_item_id)
            cart_item, created = CartItem.objects.get_or_create(user=request.user, food_item=food_item)
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, 'Item added to your cart.')
        else:
            messages.error(request, 'Invalid quantity.')
    return redirect('canteen:product')


@login_required
def update_cart_item(request, item_id):

    item = get_object_or_404(OrderItem, pk=item_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()

    return redirect('canteen:view_cart')

@login_required
def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def edit_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    
    if request.method == 'POST':
        form = EditCartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('canteen:view_cart')  # Redirect to the cart view or wherever appropriate
    else:
        # For GET request, display the current information of the cart item
        form = EditCartItemForm(instance=cart_item)

    return render(request, 'edit_cart_item.html', {'form': form, 'cart_item': cart_item})

@login_required
# def view_cart(request):
#     if request.user.is_authenticated:
#         # Retrieve the user's cart items and annotate them with the total cost
#         cart_items = CartItem.objects.filter(user=request.user).annotate(
#             total_cost=F('quantity') * F('food_item__price')
#         )

#         # Calculate the total quantity and total cost
#         total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
#         total_cost = cart_items.aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0

#         subtotal = cart_items.aggregate(total=Sum('total_cost'))['total'] or 0
#         shipping_cost = 45  # This can be a variable based on your shipping logic
#         total_cost = subtotal + shipping_cost


#         context = {
#             'cart_items': cart_items,
#             'total_quantity': total_quantity,
#             'total_cost': total_cost,

#             'subtotal': subtotal,
#             'shipping_cost': shipping_cost,
#             'total_cost': total_cost,
#         }

#         return render(request, 'cart.html', context)
#     else:
#         messages.error(request, 'You need to be logged in to view your cart.')
#         return redirect('canteen:home')


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            item.total_cost = item.quantity * item.food_item.price

        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        subtotal = sum(item.total_cost for item in cart_items)
        shipping_cost = 0  # Variable based on your shipping logic
        total_cost = subtotal + shipping_cost

        context = {
            'cart_items': cart_items,
            'total_quantity': total_quantity,
            'total_cost': total_cost,
            'subtotal': subtotal,
            'shipping_cost': shipping_cost,
        }

        return render(request, 'cart.html', context)
    else:
        messages.error(request, 'You need to be logged in to view your cart.')
        return redirect('canteen:home')

def delete_cart_item(request, item_id):

    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to delete cart items.")
        return redirect('canteen:login')

    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Cart item deleted successfully.')
    return redirect('canteen:view_cart')

@login_required
def checkout(request):
    if request.method == 'POST':
        user = request.user

        order = ...  # Get or create the order
        Receipt.objects.create(order=order)

        # Redirect to the receipt download page
        return redirect('download_receipt', order_id=order.id)

    else:
        messages.error(request, "Invalid request")
        return redirect('canteen:cart')

@login_required
def user_account(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    # You can add more context like user details if needed
    return render(request, 'user_account.html', {'orders': orders})

def checkout(request):
    if request.method == 'POST' and request.user.is_authenticated:
        with transaction.atomic():
            cart_items = CartItem.objects.filter(user=request.user)
            if cart_items.exists():
                order = Order.objects.create(user=request.user)
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order, 
                        food_item=item.food_item, 
                        quantity=item.quantity
                    )
                cart_items.delete()

                messages.success(request, 'Checkout successful.')
                return redirect('canteen:view_order', order_id=order.id)
            else:
                messages.error(request, 'Your cart is empty.')
                return redirect('canteen:view_cart')

    return redirect('canteen:view_cart')

@login_required
def download_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    receipt = get_object_or_404(Receipt, order=order)

    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF
    p.drawString(100, 100, f"Order ID: {order.id}")
    p.drawString(100, 80, f"Date: {receipt.receipt_date.strftime('%Y-%m-%d')}")
    # Add more details as needed

    # Close the PDF object cleanly
    p.showPage()
    p.save()

    # File response
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
    
def generate_receipt(request, order_id):
    # Ensure the user is authenticated and has access to this order
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    # Retrieve the order and its items
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    # Create receipt content
    receipt_lines = [
        f"Receipt for Order: {order_id}",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "-----------------------------",
        "Items Purchased:"
    ]

    total_cost = 0
    for item in order_items:
        line = f"{item.food_item.name} - Quantity: {item.quantity}, Price: Nle:{item.food_item.price}"
        receipt_lines.append(line)
        total_cost += item.quantity * item.food_item.price

    receipt_lines.append("-----------------------------")
    receipt_lines.append(f"Total Cost: Nle: {total_cost}")

    # Generate a HttpResponse with receipt content
    response_content = "\n".join(receipt_lines)
    response = HttpResponse(response_content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="receipt_order_{order_id}.txt"'

    return response

def view_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'view_order.html', {'order': order, 'order_items': order_items})

def successEmail(request):
    return render(request, 'public/contact_success.html')

def contact_us(request):
    if request.method == 'POST':
        form = ContactSubmissionForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            # Optionally, send an email to the admin here

            messages.success(request, 'Email sent successfully')
            return render(request, 'public/contact_success.html')
    else:
        form = ContactSubmissionForm()
    
    return render(request, 'public/test.html', {'form': form})


@login_required
def checkouts(request):
    cart_items = CartItem.objects.filter(user=request.user).annotate(
        total_cost=F('quantity') * F('food_item__price')
    )

    # Calculate total cost safely
    total_cost_aggregate = cart_items.aggregate(total_cost=Sum('total_cost'))
    total_cost = total_cost_aggregate.get('total_cost', 0)

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        payment_method = request.POST.get('payment_method')

        # Simulate payment processing here
        with transaction.atomic():
            cart_items = CartItem.objects.filter(user=request.user)
            if cart_items.exists():
                order = Order.objects.create(user=request.user)
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order, 
                        food_item=item.food_item, 
                        quantity=item.quantity
                    )
                cart_items.delete()

                messages.success(request, 'Checkout successful.')
                return redirect('canteen:view_order', order_id=order.id)
            else:
                messages.error(request, 'Your cart is empty.')
                return redirect('canteen:view_cart')
        # # ...

        # with transaction.atomic():
            
        #     # Clear the user's cart
        #     cart_items.delete()
        #     # Additional order recording logic here

        # messages.success(request, 'Payment successful and order placed.')
        # return redirect('canteen:view_order', order_id=order.id)  # Redirect to an order success page

    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
    }

    return render(request, 'checkouts.html', context)
