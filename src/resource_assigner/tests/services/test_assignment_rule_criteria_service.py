import pytest
from factories import AssigmentRuleCriteriaFactory, AssigmentRuleFactory, UserFactory
from resource_assigner.models import AssigmentRuleCriteria
from resource_assigner.services import AssigmentRuleCriteriaService


@pytest.fixture
def criteria_data():
    return {
        "field": "test",
        "operator": "equals",
        "assigment_rule": AssigmentRuleFactory(),
        "value": "test",
    }


@pytest.mark.django_db
def test_can_create_criteria(criteria_data):
    user = UserFactory()

    criteria = AssigmentRuleCriteriaService(user=user).create(**criteria_data)

    assert criteria.id is not None
    assert criteria.field == criteria_data["field"]
    assert criteria.operator == criteria_data["operator"]
    assert criteria.value == criteria_data["value"]


@pytest.mark.django_db
def test_can_update_criteria():
    user = UserFactory()

    criteria = AssigmentRuleCriteriaFactory()

    updated_data = {"field": "Updated Task Assignment Rule Criteria"}

    updated_criteria = AssigmentRuleCriteriaService(user=user).update(
        instance=criteria, data=updated_data
    )

    assert updated_criteria.id == criteria.id
    assert updated_criteria.field == updated_data["field"]


@pytest.mark.django_db
def test_can_delete_criteria():
    user = UserFactory()
    criteria = AssigmentRuleCriteriaFactory()

    AssigmentRuleCriteriaService(user=user).delete(instance=criteria)

    assert AssigmentRuleCriteria.objects.count() == 0
