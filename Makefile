dev:
	@echo "Starting Development Server..."
	poetry run python src/manage.py runserver

migrate:
	poetry run python src/manage.py migrate

migrations:
	poetry run python src/manage.py makemigrations

test:
	@cd src && pytest -W ignore

superuser:
	poetry run python src/manage.py makesuperuser

sync_roles:
	poetry run python src/manage.py sync_roles
