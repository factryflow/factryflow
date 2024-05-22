# All settings related to development environment goes here.
import os

from factryflow.settings.components.common import DEBUG, MIDDLEWARE, INSTALLED_APPS

# CUSTOM AUTH MIDDLEWARE SETTINGS
AUTH_MIDDEWARE = [
    "users.middleware.LoginRequiredMiddleware",
]

DISABLE_AUTH = os.getenv("DISABLE_AUTH") == "TRUE"

if not (DEBUG and DISABLE_AUTH):
    MIDDLEWARE += AUTH_MIDDEWARE


# Settings for Debug Toolbar
if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    # django-toolbar middleware
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    INTERNAL_IPS = ["127.0.0.1"]
    DEBUG_TOOLBAR_CONFIG = {
        "INTERCEPT_REDIRECTS": False,
    }
