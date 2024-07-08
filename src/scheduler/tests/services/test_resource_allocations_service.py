import pytest
from factories import (
    ResourceAllocationsFactory,
    ResourceFactory,
    TaskFactory,
    UserFactory,
)

from scheduler.models import ResourceAllocations
from scheduler.services import ResourceAllocationsService


@pytest.mark.django_db
def test_resource_allocations_create():
    user = UserFactory()

    resource = ResourceFactory()
    task = TaskFactory()

    resource_allocations_data = {
        "scheduler_run": ResourceAllocationsFactory().run_id,
        "resource": resource,
        "task": task,
    }

    resource_allocations_instance = ResourceAllocationsService(user=user).create(
        **resource_allocations_data
    )

    assert (
        resource_allocations_instance.run_id
        == resource_allocations_data["scheduler_run"]
    )
    assert resource_allocations_instance.resource == resource
    assert resource_allocations_instance.task == task


@pytest.mark.django_db
def test_resource_allocations_update():
    user = UserFactory()
    resource_allocations = ResourceAllocationsFactory()

    resource = ResourceFactory()
    task = TaskFactory()

    data = {
        "resource": resource,
        "task": task,
    }

    result = ResourceAllocationsService(user=user).update(
        instance=resource_allocations, data=data
    )

    resource_allocations_instance = result[0]

    assert resource_allocations_instance.resource == data["resource"]
    assert resource_allocations_instance.task == data["task"]


@pytest.mark.django_db
def test_resource_allocations_delete():
    user = UserFactory()
    resource_allocations = ResourceAllocationsFactory()

    assert ResourceAllocations.objects.count() == 1

    ResourceAllocationsService(user=user).delete(instance=resource_allocations)

    assert ResourceAllocations.objects.count() == 0
