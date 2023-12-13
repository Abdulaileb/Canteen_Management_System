
from django.contrib import admin
from .models import FoodCategory, FoodItem, Payment, Receipt
from django.db.models import Sum
import matplotlib.pyplot as plt



admin.site.register(FoodCategory)
admin.site.register(FoodItem)
