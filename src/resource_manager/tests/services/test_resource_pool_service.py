import pytest
from factories import ResourceFactory, WorkUnitFactory

from resource_manager.models import ResourcePool
from resource_manager.services import ResourcePoolService


@pytest.fixture
def resource_pool_data():
    return {
        "name": "Resource pool 1",
        "resources": ResourceFactory.create_batch(2),
        "work_units": WorkUnitFactory.create_batch(2),
    }


@pytest.mark.django_db
def test_can_create_resource_pool(resource_pool_data):
    resource_pool = ResourcePoolService().create(**resource_pool_data)

    assert resource_pool.name == resource_pool_data["name"]
    assert resource_pool.resources.count() == 2
    assert resource_pool.work_units.count() == 2


@pytest.mark.django_db
def test_can_update_resource_pool(resource_pool_data):
    resource_pool = ResourcePoolService().create(**resource_pool_data)

    new_name = "Resource pool 2"

    updated_resource_pool = ResourcePoolService().update(
        instance=resource_pool,
        data={
            "name": new_name,
        },
    )

    assert updated_resource_pool.name == new_name
    assert updated_resource_pool.id == resource_pool.id


@pytest.mark.django_db
def test_can_update_relationships(resource_pool_data):
    resource_pool = ResourcePoolService().create(**resource_pool_data)

    new_resources = [ResourceFactory()]
    new_work_units = [WorkUnitFactory()]

    updated_resource_pool = ResourcePoolService().update(
        instance=resource_pool,
        data={
            "resources": new_resources,
            "work_units": new_work_units,
        },
    )

    assert updated_resource_pool.id == resource_pool.id
    assert updated_resource_pool.resources.count() == 1
    assert updated_resource_pool.work_units.count() == 1


@pytest.mark.django_db
def test_can_delete_resource_pool(resource_pool_data):
    resource_pool = ResourcePoolService().create(**resource_pool_data)

    ResourcePoolService().delete(instance=resource_pool)

    assert ResourcePool.objects.count() == 0
