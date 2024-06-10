from datetime import datetime, timedelta

import pytest
from factories import (
    SchedulerRunsFactory,
    UserFactory,
)
from scheduler.models import SchedulerRuns, SchedulerStatusChoices
from scheduler.services import SchedulerRunsService


@pytest.mark.django_db
def test_scheduler_runs_create():
    user = UserFactory()

    scheduler_runs_data = {
        "start_time": datetime.now(),
        "end_time": datetime.now() + timedelta(hours=1),
        "run_duration": timedelta(hours=1),
        "details": "details description",
        "status": SchedulerStatusChoices.STARTED,
    }

    scheduler_runs_instance = SchedulerRunsService(user=user).create(
        **scheduler_runs_data
    )

    assert scheduler_runs_instance.start_time == scheduler_runs_data["start_time"]
    assert scheduler_runs_instance.end_time == scheduler_runs_data["end_time"]
    assert scheduler_runs_instance.run_duration == scheduler_runs_data["run_duration"]
    assert scheduler_runs_instance.details == scheduler_runs_data["details"]
    assert scheduler_runs_instance.status == scheduler_runs_data["status"]


@pytest.mark.django_db
def test_scheduler_runs_update():
    user = UserFactory()
    scheduler_runs = SchedulerRunsFactory()

    data = {
        "details": "scheduler runs details description",
        "status": SchedulerStatusChoices.COMPLETED,
    }

    result = SchedulerRunsService(user=user).update(instance=scheduler_runs, data=data)

    scheduler_runs_instance = result[0]

    assert scheduler_runs_instance.details == data["details"]
    assert scheduler_runs_instance.status == data["status"]


@pytest.mark.django_db
def test_scheduler_runs_delete():
    user = UserFactory()
    scheduler_runs = SchedulerRunsFactory()

    assert SchedulerRuns.objects.count() == 1

    SchedulerRunsService(user=user).delete(instance=scheduler_runs)

    assert SchedulerRuns.objects.count() == 0
