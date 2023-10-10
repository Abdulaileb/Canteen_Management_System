from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create an admin user'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = input('Enter username: ')
        email = input('Enter email: ')
        full_name = input('Enter full name: ')
        password = input('Enter password: ')
        User.objects.create_superuser(username=username, email=email, full_name=full_name, password=password)
