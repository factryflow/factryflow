dev:
	@echo "Starting Development Server..."
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

test:
	@cd src && pytest -W ignore

superuser:
	python manage.py makesuperuser

sync_roles:
	python manage.py sync_roles

create_user:
	python manage.py createuser

add_data:
	python manage.py add_data
