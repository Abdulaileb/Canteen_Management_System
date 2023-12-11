from django.db import models
from  django.utils import timezone

from  accounts.models import CustomUser
# Create your models here.

class FoodCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

# class Order(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     items = models.ManyToManyField(FoodItem, through='OrderItem')
#     order_date = models.DateTimeField(auto_now_add=True)
#     is_paid = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username
    
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(FoodItem, through='OrderItem', related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def get_total_cost(self):
        total_cost = 0
        for item in self.orderitem_set.all():
            total_cost += item.quantity * item.food_item.price  # Assuming FoodItem has a 'price' field
        return total_cost

    def __str__(self):
        return self.user.username

# class OrderedItem(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     order_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.food_item.name} x {self.quantity} - Ordered by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.food_item.name} (x{self.quantity}) in Order {self.order.id}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()

#     def __str__(self):
#         return self.order
    
class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=20)
    type = models.CharField(max_length=255)
    date = models.DateField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50)  # Cash, Credit, Mobile Money, Visa Card
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # For Mobile Money
    account_number = models.CharField(max_length=16, blank=True, null=True)  # For Visa Card
    expiring_date = models.DateField(blank=True, null=True)  # For Visa Card
    pattern = models.CharField(max_length=4, blank=True, null=True)  # For Visa Card

    def __str__(self):
        return self.order


class Receipt(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Use ForeignKey instead of OneToOneField
    receipt_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order.id)  # Return the order ID as a string
    

# class CartItemAdded(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)  # Replace FoodItem with your item model
#     added_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order #{self.id} by {self.user}"


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"
    

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
