from common.models import BaseModel
from django.db import models
from job_manager.models import Task
from resource_manager.models import Resource
from simple_history.models import HistoricalRecords

from .scheduler_run import SchedulerRuns


class ResourceIntervals(BaseModel):
    run_id = models.ForeignKey(SchedulerRuns, on_delete=models.DO_NOTHING)
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    interval_start = models.DateTimeField()
    interval_end = models.DateTimeField()

    history = HistoricalRecords(table_name="resource_intervals_history")

    class Meta:
        db_table = "resource_intervals"
