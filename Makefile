dev:
	@echo "Starting Development Server..."
	python src/manage.py runserver

migrate:
	python src/manage.py migrate

migrations:
	python src/manage.py makemigrations

