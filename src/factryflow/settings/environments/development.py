# All settings related to development environment goes here.
import os

from factryflow.settings.components.common import (
    BASE_DIR,
    DEBUG,
    INSTALLED_APPS,
    MIDDLEWARE,
)

# CUSTOM AUTH MIDDLEWARE SETTINGS
AUTH_MIDDEWARE = [
    "users.middleware.LoginRequiredMiddleware",
]

DEBUG = os.getenv("DEBUG") == "TRUE"
DISABLE_AUTH = os.getenv("DISABLE_AUTH") == "TRUE"

if not (DEBUG and DISABLE_AUTH):
    MIDDLEWARE += AUTH_MIDDEWARE


# # Settings for Debug Toolbar
# if DEBUG:
#     INSTALLED_APPS += [
#         "debug_toolbar",
#     ]

#     # django-toolbar middleware
#     MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

#     INTERNAL_IPS = ["127.0.0.1"]
#     DEBUG_TOOLBAR_CONFIG = {
#         "INTERCEPT_REDIRECTS": False,
#     }

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, "templates", "src/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": ["template_partials.templatetags.partials"],
        },
    },
]


if os.getenv("DATABASE") == "postgres":
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
