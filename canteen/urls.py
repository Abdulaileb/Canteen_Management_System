from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

app_name = 'canteen'

urlpatterns = [
    path('', views.HomePage, name='home'),
    path('product/', views.Product, name='product'),
    path('add_to_cart/<int:food_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),

    path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),

    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),

    # path('', views.dashboardPage, name='admin_dashboard'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('receipt/', views.receipt, name='receipt'),

    path('receipt_pdf/', views.receipt_pdf, name='receipt_pdf'),

    path('user_account_view/', views.user_account_view, name='user_account_view'),

    

    
]