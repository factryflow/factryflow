dev:
	@echo "Starting Development Server..."
	python src/manage.py runserver 0.0.0.0:8000

migrate:
	python src/manage.py migrate

migrations:
	python src/manage.py makemigrations

test:
	@cd src && pytest -W ignore

superuser:
	python src/manage.py makesuperuser

sync_roles:
	python src/manage.py sync_roles
