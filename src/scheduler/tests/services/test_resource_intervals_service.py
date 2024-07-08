from datetime import datetime, timedelta

import pytest
from factories import (
    SchedulerRunsFactory,
    ResourceFactory,
    ResourceIntervalsFactory,
    TaskFactory,
    UserFactory,
)
from scheduler.models import ResourceIntervals
from scheduler.services import ResourceIntervalsService


@pytest.mark.django_db
def test_resource_intervals_create():
    user = UserFactory()
    task = TaskFactory()
    resource = ResourceFactory()
    scheduler_runs = SchedulerRunsFactory()

    resource_intervals_data = {
        "scheduler_run": scheduler_runs,
        "task": task,
        "resource": resource,
        "interval_start": datetime.now(),
        "interval_end": datetime.now() + timedelta(hours=1),
    }

    resource_intervals_instance = ResourceIntervalsService(user=user).create(
        **resource_intervals_data
    )

    assert resource_intervals_instance.task == resource_intervals_data["task"]
    assert resource_intervals_instance.resource == resource_intervals_data["resource"]
    assert (
        resource_intervals_instance.interval_start
        == resource_intervals_data["interval_start"]
    )
    assert (
        resource_intervals_instance.interval_end
        == resource_intervals_data["interval_end"]
    )


@pytest.mark.django_db
def test_resource_intervals_update():
    user = UserFactory()
    resource_intervals = ResourceIntervalsFactory()

    data = {
        "interval_start": datetime.now(),
        "interval_end": datetime.now() + timedelta(hours=1),
    }

    result = ResourceIntervalsService(user=user).update(
        instance=resource_intervals, data=data
    )

    resource_intervals_instance = result[0]

    assert resource_intervals_instance.interval_start == data["interval_start"]
    assert resource_intervals_instance.interval_end == data["interval_end"]


@pytest.mark.django_db
def test_resource_intervals_delete():
    user = UserFactory()
    resource_intervals = ResourceIntervalsFactory()

    assert ResourceIntervals.objects.count() == 1

    ResourceIntervalsService(user=user).delete(instance=resource_intervals)
    assert ResourceIntervals.objects.count() == 0
