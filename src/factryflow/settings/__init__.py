from os import environ

from split_settings.tools import include

# Managing environment via `DJANGO_ENV` variable:
ENV = environ["DJANGO_ENV"]

if ENV not in ["development", "production"]:
    raise ValueError("Incorrect DJANGO_ENV value: {0}".format(ENV))

# Include settings:

base_settings = [
    "components/common.py",  # standard django settings
    # Select the right env:
    "environments/{0}.py".format(ENV),
]

# Include settings:
include(*base_settings)
