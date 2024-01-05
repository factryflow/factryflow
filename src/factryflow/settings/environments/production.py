# All settings related to productions environment goes here.
from factryflow.settings.components.common import MIDDLEWARE

DEUG = False

# Login Middleware
MIDDLEWARE += [
    "users.middleware.LoginRequiredMiddleware",
]


# postgres database
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DB_NAME',
        'USER': 'POSTGRES_USER',
        'PASSWORD': 'PASSWORD',
        'HOST': 'localhost',  # Set to the hostname or IP address of your PostgreSQL server
        'PORT': '5432',       # Default PostgreSQL port
    }
}
""" 
