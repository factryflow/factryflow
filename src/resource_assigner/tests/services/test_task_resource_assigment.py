import pytest
from django.core.exceptions import ValidationError
from factories import (
    ResourceFactory,
    ResourcePoolFactory,
    TaskFactory,
    TaskResourceAssigmentFactory,
)
from resource_assigner.models import TaskResourceAssigment
from resource_assigner.services import TaskResourceAssigmentService


@pytest.fixture
def resources():
    return [ResourceFactory(), ResourceFactory()]


@pytest.fixture
def task_resource_assignment_data(resources):
    task = TaskFactory()
    resource_group = ResourcePoolFactory()

    return {
        "task": task,
        "resource_group": resource_group,
        "resources": resources,
        "use_all_resources": False,
    }


@pytest.mark.django_db
def test_task_resource_assignment_create(task_resource_assignment_data):
    assignment = TaskResourceAssigmentService().create(**task_resource_assignment_data)

    assert TaskResourceAssigment.objects.count() == 1
    assert assignment.task == task_resource_assignment_data["task"]
    assert assignment.resource_group == task_resource_assignment_data["resource_group"]

    assert assignment.resources.all().count() == len(
        task_resource_assignment_data["resources"]
    )
    assert (
        assignment.use_all_resources
        == task_resource_assignment_data["use_all_resources"]
    )


@pytest.mark.django_db
def test_task_resource_assignment_update():
    assignment = TaskResourceAssigmentFactory()

    new_task = TaskFactory()
    new_resources = [ResourceFactory(), ResourceFactory()]

    TaskResourceAssigmentService().update(
        instance=assignment,
        data={
            "task": new_task,
            "resources": new_resources,
        },
    )

    assignment.refresh_from_db()

    assert assignment.task == new_task
    assert assignment.resources.all().count() == len(new_resources)


@pytest.mark.django_db
def test_task_resource_delete():
    assignment = TaskResourceAssigmentFactory()

    TaskResourceAssigmentService().delete(instance=assignment)

    assert TaskResourceAssigment.objects.count() == 0


@pytest.mark.django_db
def test_validation_error_raised_on_invalid_task_resource_assignment_data(
    task_resource_assignment_data, resources
):
    combinations = [
        {
            "resources": resources,
            "resource_count": 1,
        },
        {
            "resources": resources,
            "use_all_resources": True,
        },
        {
            "resources": None,
            "resource_count": 1,
            "use_all_resources": True,
        },
    ]

    for combination in combinations:
        data = task_resource_assignment_data
        data.update(combination)

        with pytest.raises(ValidationError):
            TaskResourceAssigmentService().create(**data)
