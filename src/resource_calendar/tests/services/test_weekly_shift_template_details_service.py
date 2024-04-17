from datetime import time

import pytest
from django.core.exceptions import ValidationError
from factories import UserFactory

from factories.resource_calendar_factories import WeeklyShiftTemplateFactory
from resource_calendar.services import WeeklyShiftTemplateDetailService

from resource_calendar.models import DaysOfWeek


@pytest.fixture
def detail_data():
    return {
        "day_of_week": DaysOfWeek.MONDAY.value,
        "start_time": "05:00",
        "end_time": "12:00",
    }


@pytest.mark.django_db
def test_can_create_template_detail(detail_data):
    user = UserFactory()

    detail = WeeklyShiftTemplateDetailService(user=user).create(**detail_data)

    assert detail.id is not None
    assert detail.day_of_week == detail_data["day_of_week"]
    assert detail.start_time == time(hour=5)
    assert detail.end_time == time(hour=12)


@pytest.mark.django_db
def test_wrong_time_format(detail_data):
    user = UserFactory()

    detail_data["start_time"] = "05:00:00"

    with pytest.raises(ValidationError):
        WeeklyShiftTemplateDetailService(user=user).create(
            **detail_data
        )


@pytest.mark.django_db
def test_wrong_day_of_week(detail_data):
    user = UserFactory()

    detail_data["day_of_week"] = "MON"

    with pytest.raises(ValidationError):
        WeeklyShiftTemplateDetailService(user=user).create(
            **detail_data
        )


@pytest.mark.django_db
def test_start_time_after_end_time(detail_data):
    user = UserFactory()

    detail_data["start_time"] = "13:00"

    with pytest.raises(ValidationError):
        WeeklyShiftTemplateDetailService(user=user).create(
            **detail_data
        )


@pytest.mark.django_db
def test_can_create_bulk(detail_data):
    user = UserFactory()

    detail_1 = {k: (1 if k == "day_of_week" else v) for k, v in detail_data.items()}
    detail_2 = {k: (2 if k == "day_of_week" else v) for k, v in detail_data.items()}
    detail_3 = {k: (3 if k == "day_of_week" else v) for k, v in detail_data.items()}

    details = [detail_1, detail_2, detail_3]

    WeeklyShiftTemplateDetailService(user=user).create_bulk(details=details)

    assert len(details) == 3


@pytest.mark.django_db
def test_can_delete_detail(detail_data):
    user = UserFactory()


    detail = WeeklyShiftTemplateDetailService(user=user).create(
        **detail_data
    )

    response = WeeklyShiftTemplateDetailService(user=user).delete(detail)

    assert response == True