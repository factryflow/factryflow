from datetime import datetime

import pytest
from factories import DependencyTypeFactory, UserFactory
from job_manager.models import Dependency
from job_manager.services import DependencyService


@pytest.fixture
def dependency_data():
    data = {
        "name": "test",
        "dependency_type": DependencyTypeFactory(),
        "expected_close_datetime": datetime.now(),
    }
    return data


@pytest.mark.django_db
def test_can_create_dependency(dependency_data):
    user = UserFactory()

    dependency = DependencyService(user=user).create(**dependency_data)

    assert dependency.id is not None
    assert dependency.dependency_type == dependency_data["dependency_type"]
    assert (
        dependency.expected_close_datetime == dependency_data["expected_close_datetime"]
    )


@pytest.mark.django_db
def test_can_update_dependency(dependency_data):
    user = UserFactory()

    dependency = DependencyService(user=user).create(**dependency_data)

    updated_data = {"name": "Updated Dependency"}

    updated_dependency = DependencyService(user=user).update(
        instance=dependency, data=updated_data
    )

    assert updated_dependency.id == dependency.id
    assert updated_dependency.name == updated_data["name"]


@pytest.mark.django_db
def test_can_delete_dependency(dependency_data):
    user = UserFactory()

    dependency = DependencyService(user=user).create(**dependency_data)

    DependencyService(user=user).delete(instance=dependency)

    assert Dependency.objects.count() == 0
