import pytest
from django.conf import settings
from django.core.management import call_command
from django.test import Client


@pytest.fixture()
def api_client():
    headers = {"X-API-Key": settings.API_KEY}
    client = Client(headers=headers)
    return client


@pytest.fixture(scope="function")
def load_specific_fixtures(db):
    def _load_files(filenames):
        for filename in filenames:
            call_command("loaddata", f"fixtures/{filename}.json")

    return _load_files
