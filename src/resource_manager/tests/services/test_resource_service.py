import pytest
from factories import (
    UserFactory,
    WeeklyShiftTemplateFactory,
)

from resource_manager.models import Resource, ResourceTypeChoices
from resource_manager.services import ResourceService


@pytest.fixture
def resource_data():
    return {
        "name": "Resource 1",
        "external_id": "1",
        "resource_type": ResourceTypeChoices.OPERATOR,
        "users": UserFactory.create_batch(2),
        "weekly_shift_template": WeeklyShiftTemplateFactory(),
    }


@pytest.mark.django_db
def test_can_create_resource(resource_data):
    user = UserFactory()

    resource = ResourceService(user=user).create(**resource_data)

    assert resource.name == resource_data["name"]
    assert resource.external_id == resource_data["external_id"]
    assert resource.users.count() == 2


@pytest.mark.django_db
def test_can_update_resource(resource_data):
    user = UserFactory()

    resource = ResourceService(user=user).create(**resource_data)

    new_name = "Resource 2"
    new_external_id = "2"

    updated_resource = ResourceService(user=user).update(
        instance=resource,
        data={
            "name": new_name,
            "external_id": new_external_id,
        },
    )

    assert updated_resource.name == new_name
    assert updated_resource.external_id == new_external_id
    assert updated_resource.id == resource.id


@pytest.mark.django_db
def test_can_update_relationships(resource_data):
    user = UserFactory()

    resource = ResourceService(user=user).create(**resource_data)

    new_weekly_shift_template = WeeklyShiftTemplateFactory()

    updated_resource = ResourceService(user=user).update(
        instance=resource,
        data={
            "weekly_shift_template": new_weekly_shift_template,
        },
    )

    assert updated_resource.id == resource.id
    assert updated_resource.weekly_shift_template == new_weekly_shift_template


@pytest.mark.django_db
def test_can_delete_resource(resource_data):
    user = UserFactory()

    resource = ResourceService(user=user).create(**resource_data)

    ResourceService(user=user).delete(instance=resource)

    assert Resource.objects.count() == 0
