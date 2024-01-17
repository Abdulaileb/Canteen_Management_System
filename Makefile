migrate:
	python manage.py migrate

migrate-accounts:
	python manage.py migrate accounts

migrate-canteen:
	python manage.py migrate canteen

migrations:
	python manage.py makemigrations

migrations-accounts:
	python manage.py makemigrations accounts

migrations-canteen:
	python manage.py makemigrations canteen

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