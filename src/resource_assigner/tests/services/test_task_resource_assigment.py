import pytest
from resource_assigner.models import TaskResourceAssigment
from resource_assigner.services import TaskResourceAssigmentService
from factories import ResourceFactory, TaskFactory, ResourceGroupFactory, TaskResourceAssigmentFactory, AssigmentRuleFactory, AssigmentRuleCriteriaFactory


@pytest.fixture
def task_resource_assigment_data():
    task = TaskFactory()
    resource_group = ResourceGroupFactory()
    resources = [ResourceFactory(), ResourceFactory()]

    return {
        "task": task,
        "resource_group": resource_group,
        "resources": resources,
        "use_all_resources": False,
        "is_direct": False,
    }

@pytest.mark.django_db
def test_task_resource_assigment_create(task_resource_assigment_data):
    task_resource = TaskResourceAssigmentService().create(**task_resource_assigment_data)

    assert TaskResourceAssigment.objects.count() == 1
    assert task_resource.task == task_resource_assigment_data["task"]
    assert task_resource.resource_group == task_resource_assigment_data["resource_group"]

    assert task_resource.resources.all().count() == len(task_resource_assigment_data["resources"])
    assert task_resource.use_all_resources == task_resource_assigment_data["use_all_resources"]
    assert task_resource.is_direct == task_resource_assigment_data["is_direct"]


@pytest.mark.django_db
def test_task_resource_assigment_update():
    task_resource = TaskResourceAssigmentFactory(resources=[ResourceFactory.create_batch(2)])

    new_task = TaskFactory()
    new_resource_group = ResourceGroupFactory()
    new_resources = [ResourceFactory(), ResourceFactory()]

    TaskResourceAssigmentService().update(
        instance=task_resource,
        data={
            "task": new_task,
            "resources": new_resources,
            "use_all_resources": False,
            "is_direct": True,
        },
    )

    task_resource.refresh_from_db()

    assert task_resource.task == new_task

    assert task_resource.resources.all().count() == len(new_resources)
    assert task_resource.use_all_resources == False
    assert task_resource.is_direct == True



@pytest.mark.django_db
def test_task_resource_delete():
    task_resource = TaskResourceAssigmentFactory()

    TaskResourceAssigmentService().delete(instance=task_resource)

    assert TaskResourceAssigment.objects.count() == 0