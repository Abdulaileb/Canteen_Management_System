from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.HomePage, name='home'),

    path('', views.dashboardPage, name='admin_dashboard'),
]