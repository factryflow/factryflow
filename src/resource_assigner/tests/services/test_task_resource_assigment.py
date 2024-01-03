import pytest
from django.core.exceptions import ValidationError
from factories import (
    ResourceFactory,
    ResourceGroupFactory,
    TaskFactory,
    TaskResourceAssigmentFactory,
)
from resource_assigner.models import TaskResourceAssigment
from resource_assigner.services import TaskResourceAssigmentService


@pytest.fixture
def task_resource_assignment_data():
    task = TaskFactory()
    resource_group = ResourceGroupFactory()
    resources = [ResourceFactory(), ResourceFactory()]

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
    assert assignment.is_direct == task_resource_assignment_data["is_direct"]


@pytest.mark.django_db
def test_task_resource_assignment_update():
    assignment = TaskResourceAssigmentFactory(
        resources=[ResourceFactory.create_batch(2)]
    )

    new_task = TaskFactory()
    new_resources = [ResourceFactory(), ResourceFactory()]

    TaskResourceAssigmentService().update(
        instance=assignment,
        data={
            "task": new_task,
            "resources": new_resources,
            "use_all_resources": False,
        },
    )

    assignment.refresh_from_db()

    assert assignment.task == new_task

    assert assignment.resources.all().count() == len(new_resources)
    assert assignment.use_all_resources is False


@pytest.mark.django_db
def test_task_resource_delete():
    assignment = TaskResourceAssigmentFactory()

    TaskResourceAssigmentService().delete(instance=assignment)

    assert TaskResourceAssigment.objects.count() == 0


# parameterize
@pytest.mark.parameterize(
    "combinations",
    [
        {
            "resources": [ResourceFactory(), ResourceFactory()],
            "resource_count": 1,
        },
        {
            "resources": [ResourceFactory(), ResourceFactory()],
            "use_all_resources": True,
        },
        {
            "resources": None,
            "resource_count": 1,
            "use_all_resources": True,
        },
    ],
)
@pytest.mark.django_db
def test_validation_error_raised_on_invalid_task_resource_assignment_data(
    combinations, data=task_resource_assignment_data
):
    data.update(combinations)

    with pytest.raises(ValidationError):
        TaskResourceAssigmentService().create(**data)
