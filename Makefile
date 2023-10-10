migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

run:
	python manage.py runserver

collect:
	python manage.py collectstatic

account:
	python manage.py makemigrations accounts

canteen:
	python manage.py makemigrations canteen

user:
	python manage.py createsuperuser