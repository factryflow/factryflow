import pytest
from factories import AssigmentRuleCriteriaFactory, AssigmentRuleFactory
from resource_assigner.models import AssigmentRuleCriteria, Operator
from resource_assigner.services import AssigmentRuleCriteriaService

@pytest.fixture
def task_assignment_rule_criteria_data():
    return {
        "field": "test",
        "operator": "equals",
        "assigment_rule": AssigmentRuleFactory(),
        "value": "test",
    }

@pytest.mark.django_db                              
def test_can_create_task_assignment_rule_criteria(task_assignment_rule_criteria_data):
    task_assignment_rule_criteria = AssigmentRuleCriteriaService().create(**task_assignment_rule_criteria_data)

    assert task_assignment_rule_criteria.id is not None
    assert task_assignment_rule_criteria.field == task_assignment_rule_criteria_data["field"]
    assert task_assignment_rule_criteria.operator == task_assignment_rule_criteria_data["operator"]
    assert task_assignment_rule_criteria.value == task_assignment_rule_criteria_data["value"]


@pytest.mark.django_db
def test_can_update_task_assignment_rule_criteria():
    task_assignment_rule_criteria = AssigmentRuleCriteriaFactory()

    updated_data = {"field": "Updated Task Assignment Rule Criteria"}

    updated_task_assignment_rule_criteria = AssigmentRuleCriteriaService().update(instance=task_assignment_rule_criteria, data=updated_data)

    assert updated_task_assignment_rule_criteria.id == task_assignment_rule_criteria.id
    assert updated_task_assignment_rule_criteria.field == updated_data["field"]


@pytest.mark.django_db
def test_can_delete_task_assignment_rule_criteria():
    task_assignment_rule_criteria = AssigmentRuleCriteriaFactory()

    AssigmentRuleCriteriaService().delete(instance=task_assignment_rule_criteria)

    assert AssigmentRuleCriteria.objects.count() == 0