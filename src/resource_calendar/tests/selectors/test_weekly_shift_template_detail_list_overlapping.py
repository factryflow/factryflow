import pytest
from factories.resource_calendar_factories import (
    WeeklyShiftTemplateDetailFactory,
    WeeklyShiftTemplateFactory,
)
from resource_calendar.selectors import weekly_shift_template_detail_list_overlapping


@pytest.mark.django_db
def test_no_overlap():
    day_of_week = 1
    template = WeeklyShiftTemplateFactory()
    detail1 = WeeklyShiftTemplateDetailFactory(
        weekly_shift_template=template,
        day_of_week=day_of_week,
        start_time="09:00",
        end_time="11:00",
    )
    detail2 = WeeklyShiftTemplateDetailFactory(
        weekly_shift_template=template,
        day_of_week=day_of_week,
        start_time="12:00",
        end_time="14:00",
    )

    overlapping = weekly_shift_template_detail_list_overlapping(detail1)
    assert not overlapping.exists()


@pytest.mark.django_db
def test_partial_overlap():
    template = WeeklyShiftTemplateFactory()
    day_of_week = 1  # Set a specific day of the week
    detail1 = WeeklyShiftTemplateDetailFactory(
        weekly_shift_template=template,
        day_of_week=day_of_week,
        start_time="09:00",
        end_time="12:00",
    )
    detail2 = WeeklyShiftTemplateDetailFactory(
        weekly_shift_template=template,
        day_of_week=day_of_week,
        start_time="11:00",
        end_time="13:00",
    )

    overlapping = weekly_shift_template_detail_list_overlapping(detail1)
    assert overlapping.exists()


@pytest.mark.django_db
def test_full_overlap():
    template = WeeklyShiftTemplateFactory()
    day_of_week = 1  # Set a specific day of the week
    detail1 = WeeklyShiftTemplateDetailFactory(
        weekly_shift_template=template,
        day_of_week=day_of_week,
        start_time="09:00",
        end_time="12:00",
    )
    detail2 = WeeklyShiftTemplateDetailFactory(
        weekly_shift_template=template,
        day_of_week=day_of_week,
        start_time="10:00",
        end_time="11:00",
    )

    overlapping = weekly_shift_template_detail_list_overlapping(detail1)
    assert overlapping.exists()


@pytest.mark.django_db
def test_different_days_no_overlap():
    template = WeeklyShiftTemplateFactory()
    detail1 = WeeklyShiftTemplateDetailFactory(
        weekly_shift_template=template,
        day_of_week=1,
        start_time="09:00",
        end_time="11:00",
    )
    detail2 = WeeklyShiftTemplateDetailFactory(
        weekly_shift_template=template,
        day_of_week=2,
        start_time="10:00",
        end_time="12:00",
    )

    overlapping = weekly_shift_template_detail_list_overlapping(detail1)
    assert not overlapping.exists()


@pytest.mark.django_db
def test_different_templates_no_overlap():
    template1 = WeeklyShiftTemplateFactory()
    template2 = WeeklyShiftTemplateFactory()
    detail1 = WeeklyShiftTemplateDetailFactory(
        weekly_shift_template=template1,
        day_of_week=0,
        start_time="09:00",
        end_time="11:00",
    )
    detail2 = WeeklyShiftTemplateDetailFactory(
        weekly_shift_template=template2,
        day_of_week=0,
        start_time="10:00",
        end_time="12:00",
    )

    overlapping = weekly_shift_template_detail_list_overlapping(detail1)
    assert not overlapping.exists()


@pytest.mark.django_db
def test_exclude_self():
    template = WeeklyShiftTemplateFactory()
    detail = WeeklyShiftTemplateDetailFactory(
        weekly_shift_template=template, start_time="09:00", end_time="11:00"
    )

    overlapping = weekly_shift_template_detail_list_overlapping(detail)
    assert not overlapping.exists()
