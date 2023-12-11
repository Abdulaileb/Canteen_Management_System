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

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

# View for authenticated users
# @login_required
# def index_for_authenticated(request):
#     # Render the template for authenticated users
#     return render(request, 'index.html') 

@login_required
def HomePage(request):

    food_items = FoodItem.objects.all()

    top_items = FoodItem.objects.all()[:3]

    # cart_count = sum(item.quantity for item in cart_items)




    # # user = request.user
    # orders = Order.objects.filter(user=user)
    # payments = Payment.objects.filter(order__user=user)
    # receipts = Receipt.objects.filter(order__user=user)

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

from . decorators import user_required


@user_required
# def add_to_cart(request, food_item_id):
#     # Assume quantity is passed in the request
#     quantity = int(request.POST.get('quantity', 1))
#     food_item = get_object_or_404(FoodItem, pk=food_item_id)
#     cart_item, created = CartItem.objects.get_or_create(user=request.user, item=food_item)
#     cart_item.quantity = quantity
#     cart_item.save()
#     return redirect('canteen:view_cart')

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


# @user_required
# def add_to_cart(request, food_item_id):
#     if request.method == 'POST' and request.user.is_authenticated:
#         form = AddToCartForm(request.POST)
#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']
#             food_item = get_object_or_404(FoodItem, pk=food_item_id)
#             user = request.user

#             # Create a new order for each request
#             order = Order(user=user, is_paid=False)
#             order.save()

#             # Create or update the OrderItem
#             try:
#                 order_item = OrderItem.objects.get(order=order, food_item=food_item)
#                 order_item.quantity += quantity
#             except OrderItem.DoesNotExist:
#                 order_item = OrderItem(order=order, food_item=food_item, quantity=quantity)

#             order_item.save()

#             # Create an instance of CartItemAdded to log the event
#             CartItemAdded.objects.create(user=request.user, item=food_item)

#             messages.success(request, 'Item added to your cart.')

#             return redirect('canteen:home')
#         else:
#             # If form is not valid, show an error message
#             messages.error(request, 'Invalid quantity.')
    
#     # Handle cases where the user is not authenticated or it's not a POST request
#     return redirect('canteen:home')


@login_required
def update_cart_item(request, item_id):

    item = get_object_or_404(OrderItem, pk=item_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()

    return redirect('canteen:view_cart')

# @login_required
# def delete_cart_item(request, item_id):
#     item = get_object_or_404(OrderItem, pk=item_id)
#     item.delete()
#     return redirect('canteen:view_cart')

@login_required
def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

# @login_required
# def view_cart(request):
#     if request.user.is_authenticated:
#         # Retrieve the user's cart items
#         cart_items = OrderItem.objects.filter(order__user=request.user)


        
#         # Calculate the total quantity and total price
#         total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
#         total_price = cart_items.aggregate(Sum('food_item__price'))['food_item__price__sum'] or 0

#         # total_cost = cart_items.

#         context = {
#             'cart_items': cart_items,
#             'total_quantity': total_quantity,
#             'total_price': total_price,
#             # 'total_cost':total_cost
#         }

#         return render(request, 'view_cart.html', context)
#     else:
#         messages.error(request, 'You need to be logged in to view your cart.')
#         return redirect('canteen:home')

from django.db.models import F, Sum

# @login_required
# def view_cart(request):
#     if request.user.is_authenticated:
#         # Retrieve the user's cart items
#         cart_items = OrderItem.objects.filter(order__user=request.user)

#         # Calculate the total quantity
#         total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

#         # Calculate the total cost by multiplying quantity with the price of each food item
#         # and then summing up those values.
#         total_cost = cart_items.annotate(
#             item_total=F('quantity') * F('food_item__price')
#         ).aggregate(
#             total_cost=Sum('item_total')
#         )['total_cost'] or 0

#         context = {
#             'cart_items': cart_items,
#             'total_quantity': total_quantity,
#             'total_cost': total_cost,
#         }

#         return render(request, 'view_cart.html', context)
#     else:
#         messages.error(request, 'You need to be logged in to view your cart.')
#         return redirect('canteen:home')


@login_required
def view_cart(request):
    if request.user.is_authenticated:
        # Retrieve the user's cart items and annotate them with the total cost
        cart_items = CartItem.objects.filter(user=request.user).annotate(
            total_cost=F('quantity') * F('food_item__price')
        )

        # Calculate the total quantity and total cost
        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_cost = cart_items.aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0

        subtotal = cart_items.aggregate(total=Sum('total_cost'))['total'] or 0
        shipping_cost = 45  # This can be a variable based on your shipping logic
        total_cost = subtotal + shipping_cost


        context = {
            'cart_items': cart_items,
            'total_quantity': total_quantity,
            'total_cost': total_cost,

            'subtotal': subtotal,
            'shipping_cost': shipping_cost,
            'total_cost': total_cost,
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


# def view_cart(request):

#     if request.user.is_authenticated:
#         # Retrieve the user's cart items and annotate them with the total cost
#         cart_items = CartItem.objects.filter(order__user=request.user).annotate(
#             total_cost=F('quantity') * F('food_item__price')
#         )

#         # Calculate the total quantity and total price
#         total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
#         total_cost = cart_items.aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0

#         context = {
#             'cart_items': cart_items,
#             'total_quantity': total_quantity,
#             'total_cost': total_cost,
#         }

#         return render(request, 'cart.html', context)
#     else:
#         messages.error(request, 'You need to be logged in to view your cart.')
#         return redirect('canteen:home')


# @login_required
# def checkout(request):
#     # Retrieve the user's cart items
#     cart_items = OrderItem.objects.filter(order__user=request.user)

#     context = {
#         'cart_items': cart_items,
#     }

#     return render(request, 'checkout.html', context)

@login_required
def checkout(request):
    if request.method == 'POST':
        user = request.user

        # Perform the checkout process here
        # This might include confirming the order, processing payment, etc.

        # Generate the receipt
        order = ...  # Get or create the order
        Receipt.objects.create(order=order)

        # Redirect to the receipt download page
        return redirect('download_receipt', order_id=order.id)

    else:
        messages.error(request, "Invalid request")
        return redirect('canteen:cart')

# @login_required
# def receipt(request):
#     user = request.user
#     order = Order.objects.filter(user=user, is_paid=True).latest('id')

#     # Calculate the total quantity and total cost for this order
#     total_quantity = order.orderitem_set.aggregate(Sum('quantity'))['quantity__sum'] or 0
#     total_cost = order.orderitem_set.aggregate(Sum('food_item__price'))['food_item__price__sum'] or 0

#     context = {
#         'order': order,
#         'total_quantity': total_quantity,
#         'total_cost': total_cost,
#     }

#     return render(request, 'receipt.html', context)


from django.core.exceptions import ObjectDoesNotExist

# @login_required
# def payment(request):
#     if request.method == 'POST':
#         payment_type = request.POST.get('payment_type')
#         user = request.user

#         try:
#             # Mark any existing active orders as "paid"
#             active_orders = Order.objects.filter(user=user, is_paid=False)
#             for order in active_orders:
#                 order.is_paid = True
#                 order.save()

#             # Create a new order
#             order = Order(user=user)
#             order.save()

#             # Calculate the total cost of the order by summing the costs of its associated OrderItem objects
#             total_cost = order.orderitem_set.aggregate(Sum('food_item__price'))['food_item__price__sum']

#             if total_cost is not None:
#                 # Create a payment record
#                 payment = Payment(order=order, payment_type=payment_type, amount_paid=total_cost)

#                 if payment_type == 'MobileMoney':
#                     payment.phone_number = request.POST.get('phone_number')
#                 elif payment_type == 'VisaCard':
#                     payment.account_number = request.POST.get('account_number')
#                     payment.expiring_date = request.POST.get('expiring_date')
#                     payment.pattern = request.POST.get('pattern')

#                 payment.save()

#                 # Generate a receipt
#                 receipt = Receipt(order=order)
#                 receipt.save()

#                 # Add a success message for the user
#                 messages.success(request, 'Payment successful!')

#                 # Redirect to the receipt page
#                 return redirect('canteen:receipt')
#             else:
#                 # Add an error message for the user
#                 #messages.error(request, 'Payment failed. Please try again.')
#                 return redirect('canteen:checkout')
#         except ObjectDoesNotExist:
#             # Handle the case where no active order is found
#             messages.error(request, 'No active order found. Please add items to your cart.')
#             return redirect('canteen:home')

#     return redirect('canteen:checkout')

# @login_required
# def payment(request):
#     if request.method == 'POST':
#         payment_type = request.POST.get('payment_type')
#         user = request.user

#         try:
#             # Retrieve the active order
#             active_order = Order.objects.get(user=user, is_paid=False)
            
#             # Calculate the total cost of the active order
#             total_cost = active_order.orderitem_set.aggregate(
#                 total_cost=Sum(F('quantity') * F('food_item__price'))
#             )['total_cost']

#             if total_cost is not None:
#                 # Mark the active order as "paid"
#                 active_order.is_paid = True
#                 active_order.save()

#                 # Create a payment record
#                 payment = Payment(order=active_order, payment_type=payment_type, amount_paid=total_cost)

#                 if payment_type == 'MobileMoney':
#                     payment.phone_number = request.POST.get('phone_number')
#                 elif payment_type == 'VisaCard':
#                     payment.account_number = request.POST.get('account_number')
#                     payment.expiring_date = request.POST.get('expiring_date')
#                     payment.pattern = request.POST.get('pattern')

#                 payment.save()

#                 # Generate a receipt for the active order
#                 receipt = Receipt(order=active_order)
#                 receipt.save()

#                 # Add a success message for the user
#                 messages.success(request, 'Payment successful!')

#                 # Redirect to the receipt page with the order id to view the receipt
#                 return redirect('canteen:receipt', order_id=active_order.id)
#             else:
#                 # Add an error message for the user
#                 messages.error(request, 'Payment failed. Please try again.')
#                 return redirect('canteen:checkout')

#         except Order.DoesNotExist:
#             # Handle the case where no active order is found
#             messages.error(request, 'No active order found. Please add items to your cart.')
#             return redirect('canteen:home')

#     # If not POST request, redirect to checkout
#     return redirect('canteen:receipt_pdf', order_id=active_order.id)

@login_required
def user_account(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    # You can add more context like user details if needed
    return render(request, 'user_account.html', {'orders': orders})

# @login_required
# def user_account_view(request):
#     user = request.user
#     orders = Order.objects.filter(user=user)

#     return render(request, 'home.html', {'user': user, 'orders': orders, 'payments': payments, 'receipts': receipts})

# @login_required
# def generate_pdf_receipt(request, order_id):
#     # Get the order for which you want to generate the receipt
#     order = get_object_or_404(Order, id=order_id)

#     # Create a PDF response object
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="receipt_{order.id}.pdf"'

#     # Define the page template with fixed content
#     def page_template(canvas, doc, width, height):
#         styles = getSampleStyleSheet()
#         logo = Image('static/Canteen.png', width=200, height=100)
#         email = Paragraph('Email: your@example.com', styles['Normal'])
#         telephone = Paragraph('Telephone: +1 123-456-7890', styles['Normal'])
#         date = Paragraph('Date: ' + str(order.order_date), styles['Normal'])
#         address = Paragraph('Address: Your Business Address', styles['Normal'])

#         # Position fixed content on the page
#         logo.wrapOn(canvas, width, height)
#         logo.drawOn(canvas, 50, height - 150)
#         email.wrapOn(canvas, width, height)
#         email.drawOn(canvas, 50, height - 250)
#         telephone.wrapOn(canvas, width, height)
#         telephone.drawOn(canvas, 50, height - 280)
#         date.wrapOn(canvas, width, height)
#         date.drawOn(canvas, 50, height - 310)
#         address.wrapOn(canvas, width, height)
#         address.drawOn(canvas, 50, height - 340)

#     # Create the PDF document
#     doc = SimpleDocTemplate(response, pagesize=landscape(letter))

#     # Define the table data for the receipt
#     table_data = [['Item', 'Date', 'Amount']]
    
#     # Populate the table_data with order items
#     for order_item in order.orderitem_set.all():
#         item_name = order_item.food_item.name
#         order_date = order_item.order.order_date.strftime('%Y-%m-%d %H:%M:%S')
#         amount = order_item.food_item.price * order_item.quantity
#         table_data.append([item_name, order_date, f'${amount:.2f}'])

#     # Create a table to display order details
#     table = Table(table_data, colWidths=[200, 100, 100])
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ]))

#     elements = []
#     elements.append(table)

#     # Build the PDF document
#     doc.addPageTemplates([PageTemplate(id='receipt', onPage=page_template)])
#     doc.build(elements)

#     return response


# from django.shortcuts import get_object_or_404

# def generate_pdf_receipt(request, order_id):
#     # Get the order object using the order_id
#     order = get_object_or_404(Order, pk=order_id)

#     # Create a PDF response object
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="receipt_{order.id}.pdf"'

#     # Define the page template with fixed content
#     def page_template(canvas, doc, width, height):
#         styles = getSampleStyleSheet()
#         logo = Image('static/Canteen.png', width=200, height=100)
#         email = Paragraph('Email: your@example.com', styles['Normal'])
#         telephone = Paragraph('Telephone: +1 123-456-7890', styles['Normal'])
#         date = Paragraph('Date: ' + str(order.order_date), styles['Normal'])
#         address = Paragraph('Address: Your Business Address', styles['Normal'])

#         # Position fixed content on the page
#         logo.wrapOn(canvas, width, height)
#         logo.drawOn(canvas, 50, height - 150)
#         email.wrapOn(canvas, width, height)
#         email.drawOn(canvas, 50, height - 250)
#         telephone.wrapOn(canvas, width, height)
#         telephone.drawOn(canvas, 50, height - 280)
#         date.wrapOn(canvas, width, height)
#         date.drawOn(canvas, 50, height - 310)
#         address.wrapOn(canvas, width, height)
#         address.drawOn(canvas, 50, height - 340)

#     # Create the PDF document
#     doc = SimpleDocTemplate(response, pagesize=landscape(letter))

#     # Create a list to hold your receipt content (elements)
#     elements = []  # Add your receipt content here

#     # Build the PDF document
#     doc.build(elements)

#     return response

# @login_required
# def receipt_pdf(request):
#     user = request.user
#     order = Order.objects.filter(user=user, is_paid=True).latest('id')

#     # Calculate the total quantity and total cost for this order
#     total_quantity = order.orderitem_set.aggregate(Sum('quantity'))['quantity__sum'] or 0
#     total_cost = order.orderitem_set.aggregate(Sum('food_item__price'))['food_item__price__sum'] or 0

#     # Create a response object with PDF content type
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

#     # Create a PDF document
#     doc = SimpleDocTemplate(response, pagesize=letter)

#     # Create a list of elements to include in the PDF
#     elements = []

#     # Add a business logo to the PDF (replace 'logo.png' with the path to your logo)
#     elements.append(Image('static/Canteen.png', width=200, height=100))

#     # Add business email, telephone, date, and address
#     elements.append(Spacer(1, 10))
#     elements.append(Paragraph('Email: your@example.com', getSampleStyleSheet()['Normal']))
#     elements.append(Paragraph('Telephone: +1 123-456-7890', getSampleStyleSheet()['Normal']))
#     elements.append(Paragraph('Date: ' + str(order.order_date), getSampleStyleSheet()['Normal']))
#     elements.append(Paragraph('Address: Your Business Address', getSampleStyleSheet()['Normal']))

#     # Add the receipt table
#     receipt_data = [
#         ['Order ID', 'Order Date', 'Item', 'Quantity', 'Total', 'Payment Type', 'Amount Paid'],
#         [order.id, str(order.order_date), '\n'.join([item.food_item.name for item in order.orderitem_set.all()]),
#          '\n'.join([str(item.quantity) for item in order.orderitem_set.all()]),
#          '${:.2f}'.format(total_cost), order.payment.payment_type, '${:.2f}'.format(order.payment.amount_paid)]
#     ]
#     receipt_table = Table(receipt_data, colWidths=[70, 70, 120, 50, 50, 70, 70])
#     receipt_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                                         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                                         ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

#     elements.append(Spacer(1, 12))
#     elements.append(receipt_table)

#     # Build the PDF document
#     doc.build(elements)

#     return response



# @login_required
# def receipt_pdf(request, order_id):
#     user = request.user
#     try:
#         order = Order.objects.get(user=user, is_paid=True, id=order_id)
#         # ... [rest of your receipt_pdf view code]
#     except Order.DoesNotExist:
#         # Handle the error, maybe return an error message or redirect
#         messages.error(request, 'Order not found.')
#         return redirect('canteen:home')


# def checkout(request):
#     if request.method == 'POST' and request.user.is_authenticated:
#         cart_items = CartItem.objects.filter(user=request.user)
#         if cart_items.exists():
#             order = Order.objects.create(user=request.user)
#             for item in cart_items:
#                 OrderItem.objects.create(order=order, food_item=item.food_item, quantity=item.quantity)
            
#             cart_items.delete()  # Clear the cart
#             # Process payment and other checkout steps
#             messages.success(request, 'Checkout successful.')
#         else:
#             messages.error(request, 'Your cart is empty.')
#     return redirect('canteen:home')

from django.contrib import messages
from django.shortcuts import redirect
from django.db import transaction

# def checkout(request):
#     if request.method == 'POST' and request.user.is_authenticated:
#         with transaction.atomic():  # Use an atomic transaction
#             # Get all cart items for the current user
#             cart_items = CartItem.objects.filter(user=request.user)

#             if cart_items.exists():
#                 # Create a new order for the user
#                 order = Order.objects.create(user=request.user)

#                 # For each item in the cart, create an OrderItem and associate it with the new order
#                 for item in cart_items:
#                     OrderItem.objects.create(
#                         order=order,
#                         food_item=item.food_item,
#                         quantity=item.quantity
#                     )

#                 # Clear the cart by deleting all cart items
#                 cart_items.delete()

#                 # Additional checkout logic (e.g., payment processing)

#                 messages.success(request, 'Checkout successful.')
#             else:
#                 messages.error(request, 'Your cart is empty.')
#     else:
#         messages.error(request, 'You must be logged in to checkout.')

#     return redirect('canteen:home')  # Adjust the redirect as needed

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



import io
from reportlab.pdfgen import canvas

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
    


from datetime import datetime

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

def contact_us(request):
    contactForm = ContactForm()
    if request.method == 'POST':
        print ('Done POSTED:', request.POST)
        contactForm = ContactForm(request.POST)
        if contactForm.is_valid():
         contactForm.save()

         print('Success')

        messages.success(request, 'Email sent successfully')
    else:
        form = ContactForm()
    
    return render(request, 'public/contact_success.html', {'contactForm': contactForm})

def successEmail(request):
    return render(request, 'public/contact_success.html')