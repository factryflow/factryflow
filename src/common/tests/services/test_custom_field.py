import pytest
from common.models import CustomField
from common.services import CustomFieldService
from django.contrib.contenttypes.models import ContentType
from job_manager.models import Job, Task


@pytest.fixture
def custom_field_data():
    return {
        "name": "test_name",
        "field_type": "text",
        "content_type": ContentType.objects.get_for_model(Task),
    }


@pytest.mark.django_db
def test_custom_field_create(custom_field_data):
    CustomFieldService.create(**custom_field_data)
    custom_field = CustomField.objects.first()

    assert CustomField.objects.count() == 1
    assert custom_field.name == custom_field_data["name"]
    assert custom_field.field_type == custom_field_data["field_type"]
    assert custom_field.content_type == custom_field_data["content_type"]


@pytest.mark.django_db
def test_custom_field_update(custom_field_data):
    custom_field = CustomFieldService.create(**custom_field_data)
    new_name = "new_name"
    new_field_type = "number"
    new_content_type = ContentType.objects.get_for_model(Job)

    CustomFieldService.update(
        instance=custom_field,
        data={
            "name": new_name,
            "field_type": new_field_type,
            "content_type": new_content_type,
        },
    )

    custom_field.refresh_from_db()

    assert custom_field.name == new_name
    assert custom_field.field_type == new_field_type
    assert custom_field.content_type == new_content_type


@pytest.mark.django_db
def test_custom_field_delete(custom_field_data):
    custom_field = CustomFieldService.create(**custom_field_data)

    CustomFieldService.delete(instance=custom_field)

    assert CustomField.objects.count() == 0
