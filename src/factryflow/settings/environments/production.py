# All settings related to productions environment goes here.
from factryflow.settings.components.common import MIDDLEWARE

DEUG = False

# Login Middleware
MIDDLEWARE += [
    "users.middleware.LoginRequiredMiddleware",
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
