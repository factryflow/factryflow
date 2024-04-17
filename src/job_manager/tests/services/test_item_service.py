import pytest
from factories import ItemFactory, UserFactory
from job_manager.models import Item
from job_manager.services import ItemService


@pytest.fixture
def item_data():
    data = {
        "name": "test",
        "description": "test",
        "external_id": "test",
        "notes": "test",
    }
    return data


@pytest.mark.django_db
def test_can_create_item(item_data):
    user = UserFactory()

    item = ItemService(user=user).create(**item_data)

    assert item.id is not None
    assert item.name == item_data["name"]
    assert item.description == item_data["description"]
    assert item.external_id == item_data["external_id"]
    assert item.notes == item_data["notes"]


@pytest.mark.django_db
def test_can_update_item():
    item_instance = ItemFactory()

    user = UserFactory()

    updated_data = {"name": "Updated Item"}

    updated_item = ItemService(user=user).update(item_instance, updated_data)

    assert updated_item.id == item_instance.id
    assert updated_item.name == updated_data["name"]
    assert updated_item.description == item_instance.description
    assert updated_item.external_id == item_instance.external_id
    assert updated_item.notes == item_instance.notes


@pytest.mark.django_db
def test_can_delete_item():
    item = ItemFactory()

    user = UserFactory()

    response = ItemService(user=user).delete(item)
    assert response == True

    assert not Item.objects.filter(id=item.id).exists()