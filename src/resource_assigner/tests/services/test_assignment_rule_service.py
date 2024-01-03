import pytest
from factories import AssigmentRuleFactory, ResourceGroupFactory, WorkCenterFactory
from resource_assigner.models import AssigmentRule
from resource_assigner.services import AssigmentRuleService

@pytest.fixture
def task_assignment_rule_data():
    return {
        "name": "test",
        "description": "test",
        "resource_group": ResourceGroupFactory(),
        "work_center": WorkCenterFactory(),
    }


@pytest.mark.django_db
def test_can_create_task_assignment_rule(task_assignment_rule_data):
    task_assignment_rule = AssigmentRuleService().create(**task_assignment_rule_data)

    assert task_assignment_rule.id is not None
    assert task_assignment_rule.name == task_assignment_rule_data["name"]
    assert task_assignment_rule.description == task_assignment_rule_data["description"]


@pytest.mark.django_db
def test_can_update_task_assignment_rule():
    task_assignment_rule = AssigmentRuleFactory()

    updated_data = {"name": "Updated Task Assignment Rule"}

    updated_task_assignment_rule = AssigmentRuleService().update(instance=task_assignment_rule, data=updated_data)

    assert updated_task_assignment_rule.id == task_assignment_rule.id
    assert updated_task_assignment_rule.name == updated_data["name"]


@pytest.mark.django_db
def test_can_delete_task_assignment_rule(task_assignment_rule_data):
    task_assignment_rule = AssigmentRuleService().create(**task_assignment_rule_data)

    AssigmentRuleService().delete(instance=task_assignment_rule)

    assert AssigmentRule.objects.count() == 0