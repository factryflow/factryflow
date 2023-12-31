import pytest
from factories import AssigmentRuleFactory, ResourceGroupFactory, WorkCenterFactory
from resource_assigner.models import AssigmentRule
from resource_assigner.services import AssigmentRuleService


@pytest.fixture
def assignment_rule_data():
    return {
        "name": "test",
        "description": "test",
        "resource_group": ResourceGroupFactory(),
        "work_center": WorkCenterFactory(),
        "criteria": [
            {
                "field": "test",
                "operator": "equals",
                "value": "test",
            },
            {
                "field": "test2",
                "operator": "equals",
                "value": "test2",
            },
        ],
    }


@pytest.mark.django_db
def test_can_create_assignment_rule(assignment_rule_data):
    assignment_rule = AssigmentRuleService().create(**assignment_rule_data)

    assert assignment_rule.id is not None
    assert assignment_rule.name == assignment_rule_data["name"]
    assert assignment_rule.description == assignment_rule_data["description"]
    assert assignment_rule.resource_group == assignment_rule_data["resource_group"]
    assert assignment_rule.work_center == assignment_rule_data["work_center"]
    assert assignment_rule.criteria.count() == 2


@pytest.mark.django_db
def test_can_update_assignment_rule():
    assignment_rule = AssigmentRuleFactory()

    updated_data = {"name": "Updated Task Assignment Rule"}

    updated_assignment_rule = AssigmentRuleService().update(
        instance=assignment_rule, data=updated_data
    )

    assert updated_assignment_rule.id == assignment_rule.id
    assert updated_assignment_rule.name == updated_data["name"]


@pytest.mark.django_db
def test_can_update_criteria(assignment_rule_data):
    assignment_rule = AssigmentRuleService().create(**assignment_rule_data)

    updated_criteria_data = {
        "criteria": [
            {
                "id": 1,
                "field": "test3",
            },
            {
                "field": "test4",
                "operator": "equals",
                "value": "test4",
            },
        ]
    }
    updated_assignment_rule = AssigmentRuleService().update(
        instance=assignment_rule, data=updated_criteria_data
    )

    assert updated_assignment_rule.id == assignment_rule.id
    assert updated_assignment_rule.criteria.count() == 3
    assert updated_assignment_rule.criteria.first().field == "test3"


@pytest.mark.django_db
def test_can_delete_assignment_rule(assignment_rule_data):
    assignment_rule = AssigmentRuleService().create(**assignment_rule_data)

    AssigmentRuleService().delete(instance=assignment_rule)

    assert AssigmentRule.objects.count() == 0
