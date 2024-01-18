import pytest
from django.core.exceptions import ValidationError
from factories import (
    AssigmentConstraintFactory,
    ResourceFactory,
    ResourcePoolFactory,
    TaskFactory,
    UserFactory,
    WorkUnitFactory,
)
from resource_assigner.models import AssignmentConstraint
from resource_assigner.services import AssignmentConstraintService


@pytest.fixture
def data():
    return {
        "task": TaskFactory(),
        "resource_pool": ResourcePoolFactory(),
        "required_units": 1,
    }


@pytest.mark.django_db
def test_can_create_assignment_constraint(data):
    user = UserFactory()

    constraint = AssignmentConstraintService(user=user).create(**data)

    assert AssignmentConstraint.objects.count() == 1
    assert constraint.task == data["task"]
    assert constraint.resource_pool == data["resource_pool"]
    assert constraint.required_units == data["required_units"]
    assert constraint.is_direct is True


@pytest.mark.django_db
def test_can_update_assignment_constraint():
    user = UserFactory()

    constraint = AssigmentConstraintFactory(with_task=True, with_resource_pool=True)

    new_resource_pool = ResourcePoolFactory()
    new_required_units = 2

    AssignmentConstraintService(user=user).update(
        instance=constraint,
        data={
            "resource_pool": new_resource_pool,
            "required_units": new_required_units,
        },
    )

    assert AssignmentConstraint.objects.count() == 1
    assert constraint.resource_pool == new_resource_pool
    assert constraint.required_units == new_required_units
    assert constraint.is_direct is True


@pytest.mark.django_db
def test_can_delete_assignment_constraint():
    user = UserFactory()

    constraint = AssigmentConstraintFactory()

    assert AssignmentConstraint.objects.count() == 1

    AssignmentConstraintService(user=user).delete(instance=constraint)

    assert AssignmentConstraint.objects.count() == 0


@pytest.mark.django_db
def test_validation_error_raised_on_invalid_assignment_constraint_data(data):
    user = UserFactory()

    combinations = [
        {
            "task": None,
            "assignment_rule": None,
        },
        {
            "resource_pool": None,
            "resources": None,
            "work_units": None,
        },
        {
            "resource_pool": None,
            "resources": ResourceFactory.create_batch(2),
            "work_units": WorkUnitFactory.create_batch(2),
        },
        {
            "required_units": 0,
        },
    ]

    for combination in combinations:
        data.update(combination)

        with pytest.raises(ValidationError):
            AssignmentConstraintService(user=user).create(**data)
