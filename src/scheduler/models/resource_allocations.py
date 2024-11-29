from common.models import BaseModel
from django.db import models
from job_manager.models import Task
from resource_manager.models import Resource
from simple_history.models import HistoricalRecords

from .scheduler_run import SchedulerRuns


class ResourceAllocations(BaseModel):
    run_id = models.ForeignKey(SchedulerRuns, on_delete=models.DO_NOTHING)
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)

    history = HistoricalRecords(table_name="resource_allocations_history")

    class Meta:
        db_table = "resource_allocations"
