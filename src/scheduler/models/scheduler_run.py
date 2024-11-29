from common.models import BaseModel
from django.db import models
from simple_history.models import HistoricalRecords


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

    history = HistoricalRecords(table_name="scheduler_runs_history")

    class Meta:
        db_table = "scheduler_runs"

    def __str__(self):
        return f"Scheduler Run {self.id}"

    def store_run_duration(self):
        self.run_duration = self.end_time - self.start_time
        self.save()


class SchedulerLog(BaseModel):
    id = models.AutoField(primary_key=True)
    scheduler_run = models.OneToOneField(SchedulerRuns, on_delete=models.CASCADE)
    logs = models.JSONField(default=dict, null=True, blank=True)

    history = HistoricalRecords(table_name="scheduler_logs_history")

    class Meta:
        db_table = "scheduler_logs"

    def __str__(self):
        return f"Scheduler Log for run: {self.scheduler_run.id}"
