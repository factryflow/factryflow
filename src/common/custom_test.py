import json
import pytest

class APICRUDTEST:
    """A class for dynamically testing CRUD operations for API endpoints.

    Attributes:
        api_client (object): The client for making API requests.
        endpoint (str): The endpoint URL for the API.
        model_factory (callable): A function that creates instances of the model being tested.
        payload_factory (callable): A function that generates payloads for testing.
        update_payload (dict): A dictionary containing fields to update for testing PUT requests.
    """

    def __init__(self, api_client, endpoint, model_factory, payload_factory, update_payload):
        self.api_client = api_client
        self.endpoint = endpoint
        self.model_factory = model_factory
        self.payload_factory = payload_factory
        self.update_payload = update_payload

    @pytest.fixture
    def payload(self):
        """Fixture to generate a payload for testing."""
        return self.payload_factory()

    @pytest.mark.django_db
    def test_create(self, payload):
        """Test case for creating an instance via POST request."""
        response = self.api_client.post(
            self.endpoint,
            json.dumps(payload, default=str),
            content_type="application/json",
        )

        assert response.status_code == 201

        instance = self.model_factory()
        assert instance is not None

    @pytest.mark.django_db
    def test_list(self, payload):
        """Test case for listing instances via GET request."""
        self.model_factory()

        response = self.api_client.get(self.endpoint)

        assert response.status_code == 200
        assert len(response.json()) == 1

    @pytest.mark.django_db
    def test_update(self, payload):
        """Test case for updating an instance via PUT request."""
        instance = self.model_factory()

        updated_payload = {**payload, **self.update_payload}
        response = self.api_client.put(
            f"{self.endpoint}/{instance.id}/",
            json.dumps(updated_payload, default=str),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json()["updated_field"] == "Updated Value"

    @pytest.mark.django_db
    def test_delete(self):
        """Test case for deleting an instance via DELETE request."""
        instance = self.model_factory()

        response = self.api_client.delete(f"{self.endpoint}/{instance.id}/")

        assert response.status_code == 204
        assert not self.model_factory.exists()
