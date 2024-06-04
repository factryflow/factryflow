
import pytest
from django.core.exceptions import ValidationError
from factories import UserFactory
from resource_calendar.models import DaysOfWeek
from resource_calendar.services import (
    WeeklyShiftTemplateService,
)


@pytest.fixture
def template_data_without_details():
    data = {
        "name": "Test Template",
        "description": "Test Description",
        "external_id": "1234",
        "notes": "Test Notes",
    }
    return data


@pytest.fixture
def template_data():
    data = {
        "name": "Test Template",
        "description": "Test Description",
        "details": [
            {
                "day_of_week": DaysOfWeek.TUESDAY.value,
                "start_time": "08:00",
                "end_time": "16:00",
            },
            {
                "day_of_week": DaysOfWeek.WEDNESDAY.value,
                "start_time": "08:00",
                "end_time": "16:00",
            },
            {
                "day_of_week": DaysOfWeek.THURSDAY.value,
                "start_time": "08:00",
                "end_time": "16:00",
            },
            {
                "day_of_week": DaysOfWeek.FRIDAY.value,
                "start_time": "08:00",
                "end_time": "16:00",
            },
            {
                "day_of_week": DaysOfWeek.SATURDAY.value,
                "start_time": "08:00",
                "end_time": "16:00",
            },
            {
                "day_of_week": DaysOfWeek.SUNDAY.value,
                "start_time": "08:00",
                "end_time": "16:00",
            },
        ],
    }
    return data


@pytest.mark.django_db
def test_can_create_template(template_data):
    user = UserFactory()

    template = WeeklyShiftTemplateService(user=user).create(**template_data)

    assert template.id is not None
    assert template.name == template_data["name"]
    assert template.weekly_shift_template_details.count() == len(
        template_data["details"]
    )
    assert template.weekly_shift_template_details.first().day_of_week == "Tuesday"


@pytest.mark.django_db
def test_can_update_template(template_data_without_details):
    user = UserFactory()

    template = WeeklyShiftTemplateService(user=user).create(
        **template_data_without_details
    )

    updated_data = template_data_without_details.copy()
    updated_data["name"] = "Updated Template"

    updated_template = WeeklyShiftTemplateService(user=user).update(
        template, updated_data
    )

    assert updated_template.id == template.id
    assert updated_template.name == updated_data["name"]


# TODO:
# need to update the code in order to check and create or update the details data
# @pytest.mark.django_db
# def test_details_overwrite_on_template_update(template_data):
#     user = UserFactory()

#     template = WeeklyShiftTemplateService(user=user).create(**template_data)

#     new_details = WeeklyShiftTemplateDetailFactory.build(
#         day_of_week=DaysOfWeek.MONDAY.value, start_time="09:00", end_time="17:00"
#     )

#     details_dict = new_details.__dict__

#     new_data = {"weekly_shift_template_details": details_dict}

#     updated_template = WeeklyShiftTemplateService(user=user).update(template, new_data)

#     assert updated_template.weekly_shift_template_details.count() == len(new_details)
#     assert updated_template.weekly_shift_template_details.first().start_time == time(
#         hour=9
#     )


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

    template_data["details"][0]["day_of_week"] = "Tuesday"
    template_data["details"][0]["start_time"] = "07:00"
    template_data["details"][1]["day_of_week"] = "Tuseday"
    template_data["details"][1]["start_time"] = "07:00"

    with pytest.raises(ValidationError):
        WeeklyShiftTemplateService(user=user).create(**template_data)
