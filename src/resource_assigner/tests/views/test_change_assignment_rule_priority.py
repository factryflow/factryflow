import pytest
from django.urls import reverse
from django.test import RequestFactory
from factories import AssigmentRuleFactory, WorkCenterFactory, UserFactory
from resource_assigner.views import change_assignment_rule_priority

from resource_assigner.models import AssigmentRule
from resource_assigner.services import AssigmentRuleService


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def data():
    work_center = WorkCenterFactory()

    return {
        "name": "test",
        "description": "test",
        "work_center": work_center,
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
def test_change_assignment_rule_priority_up(factory, data):
    # test to change the priority of an assignment rule in the up direction
    user = UserFactory()

    _ = AssigmentRuleService(user=user).create(**data)
    rule_2 = AssigmentRuleService(user=user).create(**data)

    url = reverse("change_assignment_rule_priority", args=[rule_2.id, "up"])
    request = factory.get(url)
    request.htmx = False

    response = change_assignment_rule_priority(request, rule_2.id, "up")

    assert response.status_code == 302

    updated_rule = AssigmentRule.objects.get(id=rule_2.id)
    assert updated_rule.order == rule_2.order - 1


@pytest.mark.django_db
def test_change_assignment_rule_priority_down(factory, data):
    # test to change the priority of an assignment rule in the down direction
    user = UserFactory()

    rule_1 = AssigmentRuleService(user=user).create(**data)
    _ = AssigmentRuleService(user=user).create(**data)

    url = reverse("change_assignment_rule_priority", args=[rule_1.id, "down"])
    request = factory.get(url)
    request.htmx = False

    response = change_assignment_rule_priority(request, rule_1.id, "down")

    assert response.status_code == 302

    updated_rule = AssigmentRule.objects.get(id=rule_1.id)
    assert updated_rule.order == rule_1.order + 1


@pytest.mark.django_db
def test_change_assignment_rule_priority_invalid_direction(factory):
    # to check if the view function returns a 400 response when an invalid direction is provided
    rule = AssigmentRuleFactory()

    url = reverse("change_assignment_rule_priority", args=[rule.id, "invalid"])
    request = factory.get(url)
    request.htmx = False

    response = change_assignment_rule_priority(request, rule.id, "invalid")

    assert response.status_code == 400


@pytest.mark.django_db
def test_change_assignment_rule_priority_rule_not_found(factory):
    # to check if the view function returns a 404 response when the rule is not found
    url = reverse("change_assignment_rule_priority", args=[999, "up"])
    request = factory.get(url)
    request.htmx = False

    response = change_assignment_rule_priority(request, 999, "up")

    assert response.status_code == 404
