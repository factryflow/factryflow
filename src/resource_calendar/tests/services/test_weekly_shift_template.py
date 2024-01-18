from datetime import time

import pytest
from django.core.exceptions import ValidationError
from factories import UserFactory
from resource_calendar.services import WeeklyShiftTemplateService


@pytest.fixture
def template_data():
    data = {
        "name": "Test Template",
        "details": [
            {"day_of_week": 0, "start_time": "08:00", "end_time": "16:00"},
            {"day_of_week": 1, "start_time": "08:00", "end_time": "16:00"},
            {"day_of_week": 2, "start_time": "08:00", "end_time": "16:00"},
            {"day_of_week": 3, "start_time": "08:00", "end_time": "16:00"},
            {"day_of_week": 4, "start_time": "08:00", "end_time": "14:00"},
        ],
    }
    return data


@pytest.mark.django_db
def test_can_create_template(template_data):
    user = UserFactory()

    template = WeeklyShiftTemplateService(user=user).create(**template_data)

    assert template.id is not None
    assert template.name == template_data["name"]
    assert template.details.count() == len(template_data["details"])
    assert template.details.first().day_of_week == 0


@pytest.mark.django_db
def test_can_update_template(template_data):
    user = UserFactory()

    template = WeeklyShiftTemplateService(user=user).create(**template_data)

    updated_data = template_data.copy()
    updated_data["name"] = "Updated Template"

    updated_template = WeeklyShiftTemplateService(user=user).update(
        template, updated_data
    )

    assert updated_template.id == template.id
    assert updated_template.name == updated_data["name"]


@pytest.mark.django_db
def test_details_overwrite_on_template_update(template_data):
    user = UserFactory()

    template = WeeklyShiftTemplateService(user=user).create(**template_data)

    new_details = template_data["details"].copy()
    new_details = new_details[1:4]
    new_details[0]["start_time"] = "09:00"
    new_data = {"details": new_details}

    updated_template = WeeklyShiftTemplateService(user=user).update(template, new_data)

    assert updated_template.details.count() == len(new_details)
    assert updated_template.details.first().start_time == time(hour=9)


# throw error on missing detail fields
@pytest.mark.django_db
def test_create_throws_value_error_on_missing_detail_fields(template_data):
    user = UserFactory()

    template_data["details"][0].pop("start_time")
    with pytest.raises(ValueError):
        WeeklyShiftTemplateService(user=user).create(**template_data)


@pytest.mark.django_db
def test_create_throws_validation_error_on_overlapping_details(template_data):
    user = UserFactory()

    template_data["details"][0]["day_of_week"] = 0
    template_data["details"][1]["day_of_week"] = 0
    template_data["details"][1]["start_time"] = "07:00"

    with pytest.raises(ValidationError):
        WeeklyShiftTemplateService(user=user).create(**template_data)
