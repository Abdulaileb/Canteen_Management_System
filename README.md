# Canteen_Management_System
This is a canteen management system that is designed to manage food ordering and payment system 

The project is designed to help with the ordering system and payment system of food at the same time

Steps in spinning up this project:

1. Activate the virtual machine through the following:
    from the command line/ terminal:
    use this command: source venv/bin/activate
2. Run requirement.txt file 
    pip -r install requirements.txt

3. Run Migrations:
    python manage.py makemigrations accounts
    python manage.py makemigrations canteen

    python manage.py makemigrations 
    python manage.py migrate accounts
    python manage.py migrate canteen

    python manage.py migrate

4. create super user 
    python manage.py createsuperuser

5. Run server :
    python manage.py runserver