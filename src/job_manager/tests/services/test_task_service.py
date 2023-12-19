import pytest
from factories import (
    DependencyFactory,
    JobFactory,
    TaskFactory,
    TaskTypeFactory,
    WorkCenterFactory,
)
from job_manager.models import Task
from job_manager.services import TaskService


@pytest.fixture
def task_data():
    data = {
        "name": "test",
        "run_time_per_unit": 1,
        "quantity": 1,
        "task_type": TaskTypeFactory(),
        "work_center": WorkCenterFactory(),
        "job": JobFactory(),
        "predecessors": [TaskFactory()],
        "successors": [TaskFactory()],
        "dependencies": [DependencyFactory()],
    }
    return data


@pytest.mark.django_db
def test_can_create_task(task_data):
    task = TaskService().create(**task_data)

    assert task.id is not None
    assert task.name == task_data["name"]
    assert task.run_time_per_unit == task_data["run_time_per_unit"]
    assert task.quantity == task_data["quantity"]
    assert task.task_type == task_data["task_type"]
    assert task.work_center == task_data["work_center"]
    assert task.predecessors.count() == len(task_data["predecessors"])
    assert task.successors.count() == len(task_data["successors"])
    assert task.dependencies.count() == len(task_data["dependencies"])
    assert task.job == task_data["job"]


@pytest.mark.django_db
def test_can_update_task(task_data):
    task = TaskService().create(**task_data)

    updated_data = {"name": "Updated Task"}

    updated_task = TaskService().update(instance=task, data=updated_data)

    assert updated_task.id == task.id
    assert updated_task.name == updated_data["name"]


@pytest.mark.django_db
def test_can_update_m2m_fields(task_data):
    task = TaskService().create(**task_data)

    updated_data = task_data.copy()
    updated_data["predecessors"] = []
    updated_data["successors"] = []
    updated_data["dependencies"] = []

    updated_task = TaskService().update(instance=task, data=updated_data)

    assert updated_task.predecessors.count() == 0
    assert updated_task.successors.count() == 0
    assert updated_task.dependencies.count() == 0


@pytest.mark.django_db
def test_can_delete_task(task_data):
    task = TaskService().create(**task_data)

    starting_count = Task.objects.count()

    TaskService().delete(task=task)

    assert Task.objects.count() == starting_count - 1
