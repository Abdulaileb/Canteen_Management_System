from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

app_name = 'canteen'

urlpatterns = [
    path('home', views.HomePage, name='home'),

    path('about', views.aboutUs, name='about'),

    path('contacts', views.contactUs, name='contacts'),

    path('', views.index_for_unauthenticated, name='index_unauthenticated'),

    path('product/', views.Product, name='product'),

    path('products/', views.Products, name='products'),

    path('contact/', views.Contact, name='contact'),

    path('add_to_cart/<int:food_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),

    path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),

    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),

    path('cart/edit/<int:cart_item_id>/', views.edit_cart_item, name='edit_cart_item'),

    path('checkout/', views.checkout, name='checkout'),
  
    path('user_account/', views.user_account, name='user_account'),


    path('generate_receipt/<int:order_id>/', views.generate_receipt, name='generate_receipt'),

    path('order/<int:order_id>/', views.view_order, name='view_order'),

    path('contact_us/', views.contact_us, name='contact_us'),

    path('contact_success/', views.successEmail, name='contact_success'),



   
    
]