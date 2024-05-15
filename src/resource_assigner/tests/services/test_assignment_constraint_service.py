import pytest
from django.core.exceptions import ValidationError
from factories import (
    AssigmentConstraintFactory,
    ResourceFactory,
    ResourceGroupFactory,
    TaskFactory,
    UserFactory,
)
from resource_assigner.models import AssignmentConstraint
from resource_assigner.services import AssignmentConstraintService


@pytest.fixture
def data():
    return {
        "task": TaskFactory(),
        "resource_group": ResourceGroupFactory(),
    }


@pytest.fixture
def assignment_constraint_data():
    return {
        "task": TaskFactory(),
        "resource_group": ResourceGroupFactory(),
        "is_direct": True,
    }


@pytest.mark.django_db
def test_can_create_assignment_constraint(assignment_constraint_data):
    user = UserFactory()

    constraint = AssignmentConstraintService(user=user).create(
        **assignment_constraint_data
    )

    assert AssignmentConstraint.objects.count() == 1
    assert constraint.task == assignment_constraint_data["task"]
    assert constraint.is_direct is True


@pytest.mark.django_db
def test_can_update_assignment_constraint():
    user = UserFactory()

    constraint = AssigmentConstraintFactory(with_task=True, with_resource_group=False)

    new_resource_group = ResourceGroupFactory()

    AssignmentConstraintService(user=user).update(
        instance=constraint,
        data={
            "resource_group": new_resource_group,
        },
    )

    assert AssignmentConstraint.objects.count() == 1
    assert constraint.is_direct is True


@pytest.mark.django_db
def test_can_delete_assignment_constraint():
    user = UserFactory()

    constraint = AssigmentConstraintFactory()

    assert AssignmentConstraint.objects.count() == 1

    response = AssignmentConstraintService(user=user).delete(instance=constraint)

    assert response == True


@pytest.mark.django_db
def test_validation_error_raised_on_invalid_assignment_constraint_data(data):
    user = UserFactory()

    combinations = [
        {
            "task": None,
            "assignment_rule": None,
        },
        {
            "resource_group": None,
            "resources": None,
        },
        {
            "resource_group": None,
            "resources": ResourceFactory.create_batch(2),
        },
    ]

    for combination in combinations:
        data.update(combination)

        with pytest.raises(ValidationError):
            AssignmentConstraintService(user=user).create(**data)
