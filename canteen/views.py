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

    # # user = request.user
    # orders = Order.objects.filter(user=user)
    # payments = Payment.objects.filter(order__user=user)
    # receipts = Receipt.objects.filter(order__user=user)

    to_render = {
        'food_items': food_items,
        # 'user': user, 'orders': orders, 'payments': payments, 'receipts': receipts
    }    
    return render(request, 'home.html', to_render)

def Product(request):

    food_items = FoodItem.objects.all()

    to_render = {
        'food_items': food_items
    }    
    return render(request, 'product.html', to_render)

def Contact(request):
    return render(request, 'contact.html',)

def dashboardPage(request):
    return render(request, 'admin_dashboard.html', )

@login_required
def add_to_cart(request, food_item_id):
    if request.method == 'POST' and request.user.is_authenticated:
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            food_item = get_object_or_404(FoodItem, pk=food_item_id)
            user = request.user

            # Create a new order for each request
            order = Order(user=user, is_paid=False)
            order.save()

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
def delete_cart_item(request, item_id):
    item = get_object_or_404(OrderItem, pk=item_id)
    item.delete()
    return redirect('canteen:view_cart')

@login_required
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

@login_required
def checkout(request):
    # Retrieve the user's cart items
    cart_items = OrderItem.objects.filter(order__user=request.user)

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'checkout.html', context)

@login_required
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


from django.core.exceptions import ObjectDoesNotExist  # Import ObjectDoesNotExist

@login_required
def payment(request):
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        user = request.user

        try:
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
        except Order.DoesNotExist:
            # Handle the case where there is no active order
            messages.error(request, 'No active order found. Please add items to your cart.')
            return redirect('canteen:home')

    return redirect('canteen:checkout')


@login_required
def user_account_view(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    payments = Payment.objects.filter(order__user=user)
    receipts = Receipt.objects.filter(order__user=user)

    return render(request, 'home.html', {'user': user, 'orders': orders, 'payments': payments, 'receipts': receipts})

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


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

@login_required
def receipt_pdf(request):
    user = request.user
    order = Order.objects.filter(user=user, is_paid=True).latest('id')

    # Calculate the total quantity and total cost for this order
    total_quantity = order.orderitem_set.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_cost = order.orderitem_set.aggregate(Sum('food_item__price'))['food_item__price__sum'] or 0

    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Create a list of elements to include in the PDF
    elements = []

    # Add a business logo to the PDF (replace 'logo.png' with the path to your logo)
    elements.append(Image('static/Canteen.png', width=200, height=100))

    # Add business email, telephone, date, and address
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('Email: your@example.com', getSampleStyleSheet()['Normal']))
    elements.append(Paragraph('Telephone: +1 123-456-7890', getSampleStyleSheet()['Normal']))
    elements.append(Paragraph('Date: ' + str(order.order_date), getSampleStyleSheet()['Normal']))
    elements.append(Paragraph('Address: Your Business Address', getSampleStyleSheet()['Normal']))

    # Add the receipt table
    receipt_data = [
        ['Order ID', 'Order Date', 'Item', 'Quantity', 'Total', 'Payment Type', 'Amount Paid'],
        [order.id, str(order.order_date), '\n'.join([item.food_item.name for item in order.orderitem_set.all()]),
         '\n'.join([str(item.quantity) for item in order.orderitem_set.all()]),
         '${:.2f}'.format(total_cost), order.payment.payment_type, '${:.2f}'.format(order.payment.amount_paid)]
    ]
    receipt_table = Table(receipt_data, colWidths=[70, 70, 120, 50, 50, 70, 70])
    receipt_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    elements.append(Spacer(1, 12))
    elements.append(receipt_table)

    # Build the PDF document
    doc.build(elements)

    return response
