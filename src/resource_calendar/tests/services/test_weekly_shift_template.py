import pytest
from resource_calendar.services import create_update_weekly_shift_template


@pytest.fixture
def template_data():
    return {"name": "Test Template"}


@pytest.fixture
def template_detail_data():
    data = [
        {"day_of_week": 0, "start_time": "08:00", "end_time": "16:00"},
        {"day_of_week": 1, "start_time": "08:00", "end_time": "16:00"},
        {"day_of_week": 2, "start_time": "08:00", "end_time": "16:00"},
        {"day_of_week": 3, "start_time": "08:00", "end_time": "16:00"},
        {"day_of_week": 4, "start_time": "08:00", "end_time": "14:00"},
    ]
    return data


@pytest.mark.django_db
def test_can_create_template(template_data, template_detail_data):
    template = create_update_weekly_shift_template(
        template_data=template_data, template_details_data=template_detail_data
    )

    assert template.id is not None
    assert template.name == template_data["name"]
    assert template.weekly_shift_template_details.count() == len(template_detail_data)
    assert template.weekly_shift_template_details.first().day_of_week == 0


@pytest.mark.django_db
def test_can_update_template(template_data):
    template = create_update_weekly_shift_template(template_data=template_data)

    updated_data = template_data.copy()
    updated_data["name"] = "Updated Template"
    updated_data["id"] = template.id

    updated_template = create_update_weekly_shift_template(template_data=updated_data)

    assert updated_template.id == template.id
    assert updated_template.name == updated_data["name"]


@pytest.mark.django_db
def test_can_update_template_details(template_data, template_detail_data):
    template = create_update_weekly_shift_template(
        template_data=template_data, template_details_data=template_detail_data
    )
    detail_to_update = template.weekly_shift_template_details.first()
    print(detail_to_update.id)

    # Update the first detail ignore the rest
    updated_detail_data = template_detail_data[0]
    updated_detail_data["start_time"] = "09:00"
    updated_detail_data["end_time"] = "17:00"
    updated_detail_data["id"] = detail_to_update.id

    template_data["id"] = template.id

    create_update_weekly_shift_template(
        template_data=template_data, template_details_data=[updated_detail_data]
    )

    # Fetch the updated detail
    updated_detail = template.weekly_shift_template_details.get(id=detail_to_update.id)

    # Assertions
    assert updated_detail.start_time == updated_detail_data["start_time"]
    assert updated_detail.end_time == updated_detail_data["end_time"]
    assert template.weekly_shift_template_details.count() == len(template_detail_data)
