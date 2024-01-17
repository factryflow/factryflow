import pytest
from factories import (
    ResourcePoolFactory,
    UserFactory,
    WeeklyShiftTemplateFactory,
    WorkUnitFactory,
)

from resource_manager.models import Resource
from resource_manager.services import ResourceService


@pytest.fixture
def resource_data():
    return {
        "name": "Resource 1",
        "external_id": "1",
        "resource_pools": ResourcePoolFactory.create_batch(2),
        "work_units": WorkUnitFactory.create_batch(2),
        "users": UserFactory.create_batch(2),
        "weekly_shift_template": WeeklyShiftTemplateFactory(),
    }


@pytest.mark.django_db
def test_can_create_resource(resource_data):
    resource = ResourceService().create(**resource_data)

    assert resource.name == resource_data["name"]
    assert resource.external_id == resource_data["external_id"]
    assert resource.resource_pools.count() == 2
    assert resource.work_units.count() == 2
    assert resource.users.count() == 2


@pytest.mark.django_db
def test_can_update_resource(resource_data):
    resource = ResourceService().create(**resource_data)

    new_name = "Resource 2"
    new_external_id = "2"

    updated_resource = ResourceService().update(
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
    resource = ResourceService().create(**resource_data)

    new_resource_pools = [ResourcePoolFactory()]
    new_weekly_shift_template = WeeklyShiftTemplateFactory()
    new_work_units = [WorkUnitFactory()]

    updated_resource = ResourceService().update(
        instance=resource,
        data={
            "resource_pools": new_resource_pools,
            "weekly_shift_template": new_weekly_shift_template,
            "work_units": new_work_units,
        },
    )

    assert updated_resource.resource_pools.count() == 1
    assert updated_resource.work_units.count() == 1
    assert updated_resource.id == resource.id
    assert updated_resource.weekly_shift_template == new_weekly_shift_template


@pytest.mark.django_db
def test_can_delete_resource(resource_data):
    resource = ResourceService().create(**resource_data)

    ResourceService().delete(instance=resource)

    assert Resource.objects.count() == 0
