import pytest
from factory.django import DjangoModelFactory

# TODO finsih this and implement on all apis


class TestCRUD:
    def __init__(
        self,
        path: str,
        payload_create: dict,
        payload_update: dict,
        factory: DjangoModelFactory,
    ):
        self.path = path
        self.payload_create = payload_create
        self.payload_update = payload_update
        self.factory = factory

    def get_url(self, id=None):
        url = self.path
        if id:
            url = f"{url}/{id}"
        return url

    @pytest.fixture
    def create_object(self):
        return self.factory.create()

    @pytest.mark.django_db
    def test_create(self, api_client):
        data = self.payload_create
        m2m_fields = [field for field in data.keys if field.endswith("_ids")]

        response = api_client.post(self.get_url(), data)
        assert (
            response.status_code == 201
        ), f"Expected status code 201, but got {response.status_code}"

        for key, value in data.items():
            if key in m2m_fields:
                # TODO implement this check if created
                pass
            else:
                assert (
                    response.data.get(key) == value
                ), f"Expected {key} to be {value}, but got {response.data.get(key)}"

    @pytest.mark.django_db
    def test_update(self, api_client, create_object):
        data = self.payload_update
        m2m_fields = [field for field in data.keys if field.endswith("_ids")]
        response = api_client.put(self.get_url(id=create_object.id), data)
        assert (
            response.status_code == 200
        ), f"Expected status code 200, but got {response.status_code}"
        create_object.refresh_from_db()
        for key, value in data.items():
            if key in m2m_fields:
                # TODO implement this check if created
                pass
            else:
                assert (
                    getattr(create_object, key) == value
                ), f"Expected {key} to be {value}, but got {getattr(create_object, key)}"

    @pytest.mark.django_db
    def test_list(self, api_client):
        response = api_client.get(self.get_url())
        assert (
            response.status_code == 200
        ), f"Expected status code 200, but got {response.status_code}"

    @pytest.mark.django_db
    def test_retrieve(self, api_client, create_object):
        response = api_client.get(self.get_url(id=create_object.id))
        assert (
            response.status_code == 200
        ), f"Expected status code 200, but got {response.status_code}"

    @pytest.mark.django_db
    def test_delete(self, api_client, create_object):
        response = api_client.delete(self.get_url(id=create_object.id))
        assert (
            response.status_code == 204
        ), f"Expected status code 204, but got {response.status_code}"
        assert not self.factory._meta.model.objects.filter(
            id=create_object.id
        ).exists(), "Object was not deleted successfully"
