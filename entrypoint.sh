#!/bin/bash

# set -e

# echo "${0}: running migrations."
# python manage.py migrate --noinput

# python manage.py runserver 0.0.0.0:8000

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic
python manage.py makesuperuser

exec "$@"
