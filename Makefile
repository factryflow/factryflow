tailwind:
	@echo "Starting Tailwind CSS Watcher..."
	sudo tailwindcss -i src/static/css/input.css -o src/static/css/output.css --watch
dev:
	@echo "Starting Development Server..."
	python src/manage.py runserver
