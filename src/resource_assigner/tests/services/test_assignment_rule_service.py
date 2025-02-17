import pytest
from factories import AssigmentRuleFactory, UserFactory, WorkCenterFactory
from resource_assigner.models import AssigmentRule, AssigmentRuleCriteria
from resource_assigner.services import AssigmentRuleService


@pytest.fixture
def assignment_rule_data():
    return {
        "name": "test",
        "description": "test",
        "work_center": WorkCenterFactory(),
        "external_id": "test",
        "notes": "description",
        "is_active": True,
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
    user = UserFactory()

    assignment_rule = AssigmentRuleService(user=user).create(**assignment_rule_data)

    assert assignment_rule.id is not None
    assert assignment_rule.name == assignment_rule_data["name"]
    assert assignment_rule.description == assignment_rule_data["description"]
    assert assignment_rule.work_center == assignment_rule_data["work_center"]
    assert assignment_rule.criteria.count() == 2


@pytest.mark.django_db
def test_can_update_assignment_rule():
    user = UserFactory()

    assignment_rule = AssigmentRuleFactory()

    updated_data = {"name": "Updated Task Assignment Rule"}

    updated_assignment_rule = AssigmentRuleService(user=user).update(
        instance=assignment_rule, data=updated_data
    )

    assert updated_assignment_rule.id == assignment_rule.id
    assert updated_assignment_rule.name == updated_data["name"]


@pytest.mark.django_db
def test_can_update_criteria(assignment_rule_data):
    user = UserFactory()

    assignment_rule = AssigmentRuleService(user=user).create(**assignment_rule_data)
    assignment_rule_criteria = AssigmentRuleCriteria.objects.filter(
        assigment_rule=assignment_rule
    ).first()

    updated_criteria_data = {
        "criteria": [
            {
                "id": assignment_rule_criteria.id,
                "field": "test3",
            },
            {
                "field": "test4",
                "operator": "equals",
                "value": "test4",
            },
        ]
    }
    updated_assignment_rule = AssigmentRuleService(user=user).update(
        instance=assignment_rule, data=updated_criteria_data
    )

    assert updated_assignment_rule.id == assignment_rule.id
    assert updated_assignment_rule.criteria.count() == 3
    assert updated_assignment_rule.criteria.first().field == "test3"


@pytest.mark.django_db
def test_can_delete_assignment_rule(assignment_rule_data):
    user = UserFactory()

    assignment_rule = AssigmentRuleService(user=user).create(**assignment_rule_data)

    AssigmentRuleService(user=user).delete(instance=assignment_rule)

    assert AssigmentRule.objects.count() == 0
