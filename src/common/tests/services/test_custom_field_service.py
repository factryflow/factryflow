import pytest
from common.models import CustomField
from common.services import CustomFieldService
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from job_manager.models import Task


@pytest.fixture
def custom_field_data():
    return {
        "name": "test_name",
        "field_type": "text",
        "label": "test_label",
        "content_type": ContentType.objects.get_for_model(Task),
    }


@pytest.mark.django_db
def test_custom_field_create(custom_field_data):
    CustomFieldService().create(**custom_field_data)
    custom_field = CustomField.objects.first()

    assert CustomField.objects.count() == 1
    assert custom_field.name == "custom_" + custom_field_data["name"]
    assert custom_field.field_type == custom_field_data["field_type"]
    assert custom_field.content_type == custom_field_data["content_type"]


@pytest.mark.django_db
def test_custom_field_update(custom_field_data):
    custom_field = CustomFieldService().create(**custom_field_data)
    new_name = "new_name"

    CustomFieldService().update(
        instance=custom_field,
        data={
            "name": new_name,
        },
    )

    custom_field.refresh_from_db()

    assert custom_field.name == "custom_" + new_name


@pytest.mark.django_db
def test_cant_update_field_type(custom_field_data):
    custom_field = CustomFieldService().create(**custom_field_data)
    new_field_type = "number"

    CustomFieldService().update(
        instance=custom_field,
        data={
            "field_type": new_field_type,
        },
    )

    custom_field.refresh_from_db()

    assert custom_field.field_type == custom_field_data["field_type"]


@pytest.mark.django_db
def test_custom_field_delete(custom_field_data):
    custom_field = CustomFieldService().create(**custom_field_data)

    CustomFieldService().delete(instance=custom_field)

    assert CustomField.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name", ["NotSnakeCase", "notSnakeCase", "not_snake_Case", "NOT_SNAKE_CASE", ""]
)
def test_on_create_validation_error_when_name_is_not_snake_case(
    name, custom_field_data
):
    custom_field_data["name"] = name

    with pytest.raises(ValidationError):
        CustomFieldService().create(**custom_field_data)
