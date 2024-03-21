from django.db import models
from common.models import BaseModel

from resource_manager.models import Resource
from job_manager.models import Task



class SchedulerStatusChoices(models.TextChoices):
    STARTED = "ST", "Started"
    COMPLETED = "CP", "Completed"
    FAILED = "FL", "Failed"
    CANCELLED = "CN", "Cancelled"

    @classmethod
    def to_dict(cls):
        """
        Convert the SchedulerStatusChoices class into a dictionary.

        Returns:
        - Dictionary where choice values are keys and choice descriptions are values.
        """
        return {choice[0]: choice[1] for choice in cls.choices}


# Create your models here.
class SchedulerRuns(BaseModel):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()             
    end_time = models.DateTimeField(null=True, blank=True) 
    run_duration = models.DurationField(null=True, blank=True) 
    details = models.TextField(null=True, blank=True)          
    status = models.CharField(
        max_length=2,
        choices=SchedulerStatusChoices.choices,
        default=SchedulerStatusChoices.STARTED,
    )

    class Meta:
        db_table = "scheduler_runs"

    def __str__(self):
        return "Scheduler Run"
    
    def store_run_duration(self):
        self.run_duration = self.end_time - self.start_time
        self.save()


class ResourceIntervals(BaseModel):
    run_id = models.ForeignKey(SchedulerRuns, on_delete=models.DO_NOTHING)
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    interval_start = models.DateTimeField()
    interval_end = models.DateTimeField()

    class Meta:
        db_table = "resource_intervals"


class ResourceAllocations(BaseModel):
    run_id = models.ForeignKey(SchedulerRuns, on_delete=models.DO_NOTHING)
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "resource_allocations"