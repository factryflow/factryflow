#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting entrypoint script..."

# Check if the database is Postgres and wait for it to be available
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Run Django management commands
echo "Running migrations..."
python manage.py migrate
echo "Collecting static files..."
python manage.py collectstatic --no-input
echo "Creating superuser..."
python manage.py makesuperuser

echo "Starting Gunicorn..."
exec gunicorn factryflow.wsgi:application --bind 0.0.0.0:80 --log-file -
