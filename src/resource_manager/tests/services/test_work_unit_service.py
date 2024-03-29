import pytest
from factories import ResourceFactory, UserFactory

from resource_manager.models import WorkUnit
from resource_manager.services import WorkUnitService


@pytest.fixture
def work_unit_data():
    return {
        "name": "Work unit 1",
    }


@pytest.mark.django_db
def test_can_create_work_unit(work_unit_data):
    user = UserFactory()

    work_unit = WorkUnitService(user=user).create(**work_unit_data)

    assert work_unit.id is not None
    assert work_unit.name == work_unit_data["name"]


@pytest.mark.django_db
def test_can_update_work_unit(work_unit_data):
    user = UserFactory()

    work_unit = WorkUnitService(user=user).create(**work_unit_data)

    new_name = "Work unit 2"

    updated_work_unit = WorkUnitService(user=user).update(
        instance=work_unit,
        data={
            "name": new_name,
        },
    )

    assert updated_work_unit.name == new_name
    assert updated_work_unit.id == work_unit.id


@pytest.mark.django_db
def test_can_delete_work_unit(work_unit_data):
    user = UserFactory()

    work_unit = WorkUnitService(user=user).create(**work_unit_data)

    WorkUnitService(user=user).delete(instance=work_unit)

    assert WorkUnit.objects.count() == 0
