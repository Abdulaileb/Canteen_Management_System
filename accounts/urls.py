# from django.urls import path

# from django.contrib.auth import views as auth_views
# from .views import *

# from . import views

# app_name = 'accounts'

# urlpatterns = [
#     path('signup/', views.student_user_registration, name='studentSignUp'),

#     path('login/', views.loginPage, name='signIn'),
# ]


from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('dashboard', views.Dashboard, name='dashboard'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Add other app URLs here
    path('orders/income-chart/', views.create_income_chart, name='income_chart'),


     ############### Admin Adding some data

    path('manage-food-category/', views.manage_food_category, name='manage_foodCategory'),
    path('manage-food-item/', views.manage_food_items, name='manage_foodItems'),

    path('manage-inventory/', views.manage_inventory_category, name='manage-inventory'),

    path('orders/', views.OrderListView, name='view_orders'),

    path('manage-employees/', views.register_admin, name='manage-employees'),
    path('manage-students/', views.user_list, name='manage-students'),

    path('summary_report/', views.summary_report, name='summary_report'),

    path('management/report/', views.management_report, name='management_report'),

    path('receipt/', views.view_receipts, name='view_receipts'),
]
