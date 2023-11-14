
from django.contrib import admin
from .models import FoodCategory, FoodItem, Payment, Receipt
from django.db.models import Sum
import matplotlib.pyplot as plt

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'order_date', 'is_paid')
#     list_filter = ('is_paid',)

#     def total_income(self, obj):
#         total = obj.orderitem_set.aggregate(Sum('food_item__price'))['food_item__price__sum']
#         return f"${total:.2f}"
    
#     def create_income_chart(self, request):
#         orders = Order.objects.filter(is_paid=True)
#         income = [order.orderitem_set.aggregate(Sum('food_item__price'))['food_item__price__sum'] or 0 for order in orders]
        
#         plt.plot(income)
#         plt.xlabel('Orders')
#         plt.ylabel('Income')
#         plt.title('Income Chart')
#         plt.savefig('income_chart.png')
#         plt.close()

#         with open('income_chart.png', 'rb') as chart:
#             from django.http import FileResponse
#             return FileResponse(chart)

#     total_income.short_description = 'Total Income'

admin.site.register(FoodCategory)
admin.site.register(FoodItem)

admin.site.register(Payment)
admin.site.register(Receipt)
