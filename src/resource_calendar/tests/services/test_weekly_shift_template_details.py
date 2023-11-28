from datetime import time

import pytest
from django.core.exceptions import ValidationError
from factories.resource_calendar_factories import WeeklyShiftTemplateFactory
from resource_calendar.services import create_update_weekly_shift_template_detail


@pytest.fixture
def detail_data():
    return {
        "day_of_week": 0,
        "start_time": "05:00",
        "end_time": "12:00",
    }


@pytest.mark.django_db
def test_can_create_template_detail(detail_data):
    template = WeeklyShiftTemplateFactory()

    template_detail = create_update_weekly_shift_template_detail(
        detail_data=detail_data, weekly_shift_template=template
    )

    assert template_detail.id is not None
    assert template_detail.weekly_shift_template == template
    assert template_detail.day_of_week == detail_data["day_of_week"]
    assert template_detail.start_time == time(hour=5)
    assert template_detail.end_time == time(hour=12)


@pytest.mark.django_db
def test_can_update_template_detail(detail_data):
    template = WeeklyShiftTemplateFactory()

    # Create an initial template detail
    initial_detail = create_update_weekly_shift_template_detail(
        detail_data=detail_data, weekly_shift_template=template
    )

    # Prepare updated data, including the ID of the initial detail
    updated_data = detail_data.copy()
    updated_data["start_time"] = "08:00"
    updated_data["end_time"] = "16:00"
    updated_data[
        "id"
    ] = initial_detail.id  # Include the ID for the detail to be updated

    # Update the template detail
    updated_detail = create_update_weekly_shift_template_detail(
        detail_data=updated_data
    )

    # Assertions to check if the detail has been updated successfully
    assert updated_detail.id == initial_detail.id
    assert updated_detail.weekly_shift_template == template
    assert updated_detail.start_time == time(hour=8)
    assert updated_detail.end_time == time(hour=16)


@pytest.mark.django_db
def test_invalid_day_of_week(detail_data):
    detail_data["day_of_week"] = 7
    template = WeeklyShiftTemplateFactory()

    with pytest.raises(ValidationError):
        create_update_weekly_shift_template_detail(
            detail_data=detail_data, weekly_shift_template=template
        )


@pytest.mark.django_db
def test_start_time_after_end_time(detail_data):
    detail_data["start_time"] = "13:00"
    template = WeeklyShiftTemplateFactory()

    with pytest.raises(ValidationError):
        create_update_weekly_shift_template_detail(
            detail_data=detail_data, weekly_shift_template=template
        )


@pytest.mark.django_db
def test_start_time_with_seconds_invalid(detail_data):
    detail_data["start_time"] = "12:00:00"
    template = WeeklyShiftTemplateFactory()

    with pytest.raises(ValidationError):
        create_update_weekly_shift_template_detail(
            detail_data=detail_data, weekly_shift_template=template
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "new_start_time, new_end_time",
    [
        ("05:00", "12:00"),  # Full overlap
        ("04:00", "06:00"),  # Partial overlap, starts before and ends during existing
        ("06:00", "13:00"),  # Partial overlap, starts during and ends after existing
        ("11:00", "13:00"),  # Partial overlap, starts during and ends after existing
    ],
)
def test_times_cant_overlap(detail_data, new_start_time, new_end_time):
    template = WeeklyShiftTemplateFactory()

    create_update_weekly_shift_template_detail(
        detail_data=detail_data, weekly_shift_template=template
    )

    overlapping_detail_data = detail_data.copy()
    overlapping_detail_data["start_time"] = new_start_time
    overlapping_detail_data["end_time"] = new_end_time

    with pytest.raises(ValidationError):
        create_update_weekly_shift_template_detail(
            detail_data=overlapping_detail_data, weekly_shift_template=template
        )


@pytest.mark.django_db
def test_times_do_not_overlap(detail_data):
    template = WeeklyShiftTemplateFactory()

    # Create the first template detail
    first_detail = create_update_weekly_shift_template_detail(
        detail_data=detail_data, weekly_shift_template=template
    )

    # Create a non-overlapping second detail
    non_overlapping_detail_data = detail_data.copy()
    non_overlapping_detail_data["start_time"] = "13:00"
    non_overlapping_detail_data["end_time"] = "15:00"

    second_detail = create_update_weekly_shift_template_detail(
        detail_data=non_overlapping_detail_data, weekly_shift_template=template
    )

    # Assertions to ensure both details are created successfully
    assert first_detail.id is not None
    assert second_detail.id is not None
    assert first_detail.weekly_shift_template == template
    assert second_detail.weekly_shift_template == template
    assert second_detail.start_time == time(hour=13)
    assert second_detail.end_time == time(hour=15)
