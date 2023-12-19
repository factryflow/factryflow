import pytest
from factories import ResourceFactory

from resource_manager.models import ResourceGroup
from resource_manager.services import ResourceGroupService


@pytest.fixture
def resource_group_data():
    return {
        "name": "Resource Group 1",
        "resources": ResourceFactory.create_batch(2),
    }


@pytest.mark.django_db
def test_can_create_resource_group(resource_group_data):
    resource_group = ResourceGroupService().create(**resource_group_data)

    assert resource_group.name == resource_group_data["name"]
    assert resource_group.resources.count() == 2


@pytest.mark.django_db
def test_can_update_resource_group(resource_group_data):
    resource_group = ResourceGroupService().create(**resource_group_data)

    new_name = "Resource Group 2"

    updated_resource_group = ResourceGroupService().update(
        instance=resource_group,
        data={
            "name": new_name,
        },
    )

    assert updated_resource_group.name == new_name
    assert updated_resource_group.id == resource_group.id


@pytest.mark.django_db
def test_can_update_relationships(resource_group_data):
    resource_group = ResourceGroupService().create(**resource_group_data)

    new_resources = [ResourceFactory()]

    updated_resource_group = ResourceGroupService().update(
        instance=resource_group,
        data={
            "resources": new_resources,
        },
    )

    assert updated_resource_group.resources.count() == 1
    assert updated_resource_group.id == resource_group.id


@pytest.mark.django_db
def test_can_delete_resource_group(resource_group_data):
    resource_group = ResourceGroupService().create(**resource_group_data)

    ResourceGroupService().delete(instance=resource_group)

    assert ResourceGroup.objects.count() == 0
