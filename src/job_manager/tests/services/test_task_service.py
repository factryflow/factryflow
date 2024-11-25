import pytest
from factories import (
    DependencyFactory,
    JobFactory,
    TaskFactory,
    TaskTypeFactory,
    UserFactory,
    WorkCenterFactory,
    ItemFactory,
)
from job_manager.models import Task, WorkCenter
from job_manager.services import TaskService, WorkCenterService


@pytest.fixture
def task_data():
    data = {
        "name": "test",
        "run_time_per_unit": 1,
        "quantity": 1,
        "task_type": TaskTypeFactory(),
        "work_center": WorkCenterFactory(),
        "job": JobFactory(name="test", due_date="2021-01-01"),
        "item": ItemFactory(),
        "predecessors": [TaskFactory()],
        "dependencies": [DependencyFactory()],
    }
    return data


@pytest.fixture
def work_center_data():
    data = {"name": "name", "notes": "notes"}
    return data


@pytest.mark.django_db
def test_can_create_work_center(work_center_data):
    user = UserFactory()

    work_center = WorkCenterService(user=user).create(**work_center_data)

    assert work_center.id is not None
    assert work_center.name == work_center_data["name"]
    assert work_center.notes == work_center_data["notes"]


@pytest.mark.django_db
def test_can_update_work_center():
    user = UserFactory()

    work_center_instance = WorkCenterFactory()
    updated_data = {"name": "Updated Work Center"}

    updated_work_center = WorkCenterService(user=user).update(
        work_center_instance, updated_data
    )

    assert updated_work_center.id == work_center_instance.id
    assert updated_work_center.name == updated_data["name"]


@pytest.mark.django_db
def test_can_delete_work_center():
    user = UserFactory()

    work_center_instance = WorkCenterFactory()

    objects_count = WorkCenter.objects.count()

    WorkCenterService(user=user).delete(work_center_instance)

    assert WorkCenter.objects.count() == objects_count - 1


@pytest.mark.django_db
def test_can_create_task(task_data):
    user = UserFactory()

    task = TaskService(user=user).create(**task_data)

    assert task.id is not None
    assert task.name == task_data["name"]
    assert task.run_time_per_unit == task_data["run_time_per_unit"]
    assert task.quantity == task_data["quantity"]
    assert task.item == task_data["item"]
    assert task.task_type == task_data["task_type"]
    assert task.work_center == task_data["work_center"]
    assert task.predecessors.count() == len(task_data["predecessors"])
    assert task.dependencies.count() == len(task_data["dependencies"])
    assert task.job == task_data["job"]


@pytest.mark.django_db
def test_can_update_task(task_data):
    user = UserFactory()

    task = TaskService(user=user).create(**task_data)

    updated_data = {"name": "Updated Task"}

    updated_task = TaskService(user=user).update(instance=task, data=updated_data)

    assert updated_task.id == task.id
    assert updated_task.name == updated_data["name"]


@pytest.mark.django_db
def test_can_update_m2m_fields(task_data):
    user = UserFactory()

    task = TaskService(user=user).create(**task_data)

    updated_data = task_data.copy()
    updated_data["predecessors"] = []
    updated_data["dependencies"] = []

    updated_task = TaskService(user=user).update(instance=task, data=updated_data)

    assert updated_task.predecessors.count() == 0
    assert updated_task.dependencies.count() == 0


@pytest.mark.django_db
def test_can_delete_task(task_data):
    user = UserFactory()

    task = TaskService(user=user).create(**task_data)

    starting_count = Task.objects.count()

    TaskService(user=user).delete(task=task)

    assert Task.objects.count() == starting_count - 1
