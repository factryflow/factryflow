import pytest
from factories import (
    AssigmentRuleFactory,
    TaskFactory,
    TaskResourceAssigmentFactory,
    UserFactory,
)
from resource_assigner.models import TaskResourceAssigment
from resource_assigner.services import TaskResourceAssigmentService


@pytest.fixture
def data():
    return {
        "task": TaskFactory(),
        "assigment_rule": AssigmentRuleFactory(),
    }


@pytest.mark.django_db
def test_can_create_task_resource_assignment(data):
    user = UserFactory()

    assignment = TaskResourceAssigmentService(user=user).create(**data)

    assert TaskResourceAssigment.objects.count() == 1
    assert assignment.task == data["task"]
    assert assignment.assigment_rule == data["assigment_rule"]


@pytest.mark.django_db
def test_can_update_task_resource_assignment():
    user = UserFactory()

    assignment = TaskResourceAssigmentFactory()

    new_task = TaskFactory()

    TaskResourceAssigmentService(user=user).update(
        instance=assignment,
        data={
            "task": new_task,
        },
    )

    assert TaskResourceAssigment.objects.count() == 1
    assert assignment.task == new_task


@pytest.mark.django_db
def test_can_delete_task_resource_assignment():
    user = UserFactory()

    assignment = TaskResourceAssigmentFactory()

    assert TaskResourceAssigment.objects.count() == 1

    TaskResourceAssigmentService(user=user).delete(instance=assignment)

    assert TaskResourceAssigment.objects.count() == 0
