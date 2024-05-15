import pytest
from factories import UserFactory

from resource_manager.models import ResourceGroup
from resource_manager.services import ResourceGroupService


@pytest.fixture
def resource_group_data():
    return {
        "name": "Resource group 1",
    }


@pytest.mark.django_db
def test_can_create_resource_group(resource_group_data):
    user = UserFactory()

    resource_group = ResourceGroupService(user=user).create(**resource_group_data)

    assert resource_group.name == resource_group_data["name"]
    assert ResourceGroup.objects.count() == 1


@pytest.mark.django_db
def test_can_update_resource_group(resource_group_data):
    user = UserFactory()

    resource_group = ResourceGroupService(user=user).create(**resource_group_data)

    new_name = "Resource pool 2"

    updated_resource_group = ResourceGroupService(user=user).update(
        instance=resource_group,
        data={
            "name": new_name,
        },
    )

    assert updated_resource_group.name == new_name
    assert updated_resource_group.id == resource_group.id


@pytest.mark.django_db
def test_can_delete_resource_pool(resource_group_data):
    user = UserFactory()

    resource_pool = ResourceGroupService(user=user).create(**resource_group_data)

    ResourceGroupService(user=user).delete(instance=resource_pool)

    assert ResourceGroup.objects.count() == 0
