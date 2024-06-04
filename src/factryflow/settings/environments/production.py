# All settings related to productions environment goes here.
from pathlib import Path
from factryflow.settings.components.common import MIDDLEWARE

# Login Middleware
MIDDLEWARE += [
    "users.middleware.LoginRequiredMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

# postgres database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_URL = "/static/"
STATIC_ROOT = "/app/src/staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "factryflow-stg.azurewebsites.net",
    "factryflow-comp-stg.azurewebsites.net"
]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'https://localhost',
    'http://localhost:1337',
    'https://factryflow-stg.azurewebsites.net',
    'https://factryflow-comp-stg.azurewebsites.net'
]
