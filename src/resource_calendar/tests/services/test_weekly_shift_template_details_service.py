from datetime import time

import pytest
from django.core.exceptions import ValidationError
from factories import UserFactory, WeeklyShiftTemplateFactory

from resource_calendar.services import WeeklyShiftTemplateDetailService

from resource_calendar.models import DaysOfWeek, WeeklyShiftTemplateDetail


@pytest.fixture
def detail_data():
    return {
        "weekly_shift_template": WeeklyShiftTemplateFactory(),
        "day_of_week": DaysOfWeek.MONDAY.value,
        "start_time": "05:00",
        "end_time": "12:00",
    }


@pytest.fixture
def multiple_detail_data():
    data_list = [
        {
            "day_of_week": DaysOfWeek.MONDAY.value,
            "start_time": "05:00",
            "end_time": "12:00",
        },
        {
            "day_of_week": DaysOfWeek.TUESDAY.value,
            "start_time": "05:00",
            "end_time": "12:00",
        },
        {
            "day_of_week": DaysOfWeek.WEDNESDAY.value,
            "start_time": "05:00",
            "end_time": "12:00",
        },
        {
            "day_of_week": DaysOfWeek.THURSDAY.value,
            "start_time": "05:00",
            "end_time": "12:00",
        },
    ]

    return data_list


@pytest.mark.django_db
def test_can_create_template_detail(detail_data):
    user = UserFactory()

    detail = WeeklyShiftTemplateDetailService(user=user).create(**detail_data)

    assert detail.id is not None
    assert detail.weekly_shift_template == detail_data["weekly_shift_template"]
    assert detail.day_of_week == detail_data["day_of_week"]
    assert detail.start_time == time(hour=5)
    assert detail.end_time == time(hour=12)


@pytest.mark.django_db
def test_wrong_time_format(detail_data):
    user = UserFactory()

    detail_data["start_time"] = "05:00:00"

    with pytest.raises(ValidationError):
        WeeklyShiftTemplateDetailService(user=user).create(**detail_data)


@pytest.mark.django_db
def test_wrong_day_of_week(detail_data):
    user = UserFactory()

    detail_data["day_of_week"] = "MON"

    with pytest.raises(ValidationError):
        WeeklyShiftTemplateDetailService(user=user).create(**detail_data)


@pytest.mark.django_db
def test_start_time_after_end_time(detail_data):
    user = UserFactory()

    detail_data["start_time"] = "13:00"

    with pytest.raises(ValidationError):
        WeeklyShiftTemplateDetailService(user=user).create(**detail_data)


@pytest.mark.django_db
def test_can_create_bulk(multiple_detail_data):
    user = UserFactory()

    weekly_shift_template = WeeklyShiftTemplateFactory()

    WeeklyShiftTemplateDetailService(user=user).create_bulk(
        weekly_shift_template, multiple_detail_data
    )

    assert WeeklyShiftTemplateDetail.objects.count() == len(multiple_detail_data)


@pytest.mark.django_db
def test_can_delete_detail(detail_data):
    user = UserFactory()

    detail = WeeklyShiftTemplateDetailService(user=user).create(**detail_data)

    response = WeeklyShiftTemplateDetailService(user=user).delete(detail)

    assert response == True
