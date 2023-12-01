"""
WSGI config for factryflow project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'factryflow.settings')

application = get_wsgi_application()
call_command("makemigrations", "--noinput")
call_command("migrate")
call_command("collectstatic", "--noinput")

