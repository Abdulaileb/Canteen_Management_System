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

class Order(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(FoodItem, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

# class Payment(models.Model):
#     order = models.OneToOneField(Order, on_delete=models.CASCADE)
#     payment_type = models.CharField(max_length=50)  # Cash, Credit, Mobile Money
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50)  # Cash, Credit, Mobile Money, Visa Card
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # For Mobile Money
    account_number = models.CharField(max_length=16, blank=True, null=True)  # For Visa Card
    expiring_date = models.DateField(blank=True, null=True)  # For Visa Card
    pattern = models.CharField(max_length=4, blank=True, null=True)  # For Visa Card

class Receipt(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    receipt_date = models.DateTimeField(auto_now_add=True)