from datetime import datetime

import pytest
from factories import DependencyTypeFactory, JobFactory, TaskFactory
from job_manager.models import Dependency
from job_manager.services import DependencyService


@pytest.fixture
def dependency_data():
    data = {
        "name": "test",
        "dependency_type": DependencyTypeFactory(),
        "tasks": [TaskFactory(), TaskFactory()],
        "jobs": [JobFactory(), JobFactory()],
        "expected_close_datetime": datetime.now(),
    }
    return data


@pytest.mark.django_db
def test_can_create_dependency(dependency_data):
    dependency = DependencyService().create(**dependency_data)

    assert dependency.id is not None
    assert dependency.dependency_type == dependency_data["dependency_type"]
    assert (
        dependency.expected_close_datetime == dependency_data["expected_close_datetime"]
    )

    assert dependency.tasks.count() == len(dependency_data["tasks"])
    assert dependency.jobs.count() == len(dependency_data["jobs"])


@pytest.mark.django_db
def test_can_update_dependency(dependency_data):
    dependency = DependencyService().create(**dependency_data)

    updated_data = {"name": "Updated Dependency"}

    updated_dependency = DependencyService().update(
        instance=dependency, data=updated_data
    )

    assert updated_dependency.id == dependency.id
    assert updated_dependency.name == updated_data["name"]


@pytest.mark.django_db
def test_can_update_m2m_fields(dependency_data):
    dependency = DependencyService().create(**dependency_data)

    updated_data = {
        "tasks": [TaskFactory()],
        "jobs": [JobFactory()],
    }

    updated_dependency = DependencyService().update(
        instance=dependency, data=updated_data
    )

    assert updated_dependency.id == dependency.id
    assert updated_dependency.tasks.count() == len(updated_data["tasks"])
    assert updated_dependency.jobs.count() == len(updated_data["jobs"])


@pytest.mark.django_db
def test_can_delete_dependency(dependency_data):
    dependency = DependencyService().create(**dependency_data)

    DependencyService().delete(instance=dependency)

    assert Dependency.objects.count() == 0
