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

    # path('manage_food_category/', views.manage_food_category, name='manage_foodCategory'),

    ################# ASSET CONDITION #######################
    path('manage_food_category/', views.manage_food_category, name='manage_foodCategory'),
    path('manage_food_category/create/', views.manage_food_category, {'action': 'create'}, name='create_foodCategory'),
    path('manage_food_category/update/<int:pk>/', views.manage_food_category, {'action': 'update'}, name='update_foodCategory'),
    path('manage_food_category/delete/<int:pk>/', views.manage_food_category, {'action': 'delete'}, name='delete_foodCategory'),
    
    ################# FOOD ITEMS #######################
    path('manage_food_item/', views.manage_food_items, name='manage_foodItems'),
    path('manage_food_item/create/', views.manage_food_items, {'action': 'create'}, name='create_foodItems'),
    path('manage_food_item/update/<int:pk>/', views.manage_food_items, {'action': 'update'}, name='update_foodItems'),
    path('manage_food_item/delete/<int:pk>/', views.manage_food_items, {'action': 'delete'}, name='delete_foodItems'),

    ################# CANTEEN ITEMS #######################
    path('manage_inventory/', views.manage_inventory_category, name='manage_inventory'),
    path('manage_inventory/create/', views.manage_inventory_category, {'action': 'create'}, name='create_inventory'),
    path('manage_inventory/update/<int:pk>/', views.manage_inventory_category, {'action': 'update'}, name='update_inventory'),
    path('manage_inventory/delete/<int:pk>/', views.manage_inventory_category, {'action': 'delete'}, name='delete_inventory'),

    path('orders/', views.OrderListView, name='view_orders'),

    path('manage-employees/', views.register_admin, name='manage-employees'),
    
    ################# USERS ITEMS #######################
    path('manage_users/', views.user_list, name='manage_users'),
    path('manage_users/create/', views.user_list, {'action': 'create'}, name='create_users'),
    path('manage_users/update/<int:pk>/', views.user_list, {'action': 'update'}, name='update_users'),
    path('manage_users/delete/<int:pk>/', views.user_list, {'action': 'delete'}, name='delete_users'),

    path('update_users/<int:user_id>', views.update_users, name='update_users'),

    path('summary_report/', views.summary_report, name='summary_report'),

    path('management/report/', views.management_report, name='management_report'),

    path('view_receipts/', views.all_receipts, name='view_receipts'),

    path('view_emails/', views.email_submissions, name='view_emails'),
]
