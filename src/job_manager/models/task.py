from common.models import BaseModel
from django.db import models
from simple_history.models import HistoricalRecords

from job_manager.models.job import Job


class WorkCenter(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    notes = models.TextField(blank=True, null=True)

    history = HistoricalRecords(table_name="work_center_history")

    class Meta:
        db_table = "work_center"


class TaskType(BaseModel):
    name = models.CharField(max_length=150)

    history = HistoricalRecords(table_name="task_type_history")

    class Meta:
        db_table = "task_type"


class TaskStatusChoices(models.TextChoices):
    NOT_STARTED = "NS", "Not Started"
    IN_PROGRESS = "IP", "In Progress"
    COMPLETED = "CM", "Completed"


class Task(BaseModel):
    # core fields
    id = models.AutoField(primary_key=True)
    external_id = models.CharField(max_length=150, blank=True)
    name = models.CharField(max_length=150)
    setup_time = models.PositiveIntegerField()
    run_time_per_unit = models.PositiveIntegerField()
    teardown_time = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    planned_start_datetime = models.DateTimeField(blank=True, null=True)
    planned_end_datetime = models.DateTimeField(blank=True, null=True)
    item = models.CharField(max_length=250, blank=True, null=True)
    task_status = models.CharField(
        max_length=2,
        choices=TaskStatusChoices.choices,
        default=TaskStatusChoices.NOT_STARTED,
    )

    # relationship fields
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks_type"
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="tasks", blank=True, null=True
    )
    work_center = models.ForeignKey(
        WorkCenter, on_delete=models.DO_NOTHING, related_name="tasks", default=1
    )
    predecessors = models.ManyToManyField(
        "self", symmetrical=False, related_name="successors", blank=True
    )
    dependencies = models.ManyToManyField("Dependency", related_name="tasks")

    # special fields
    history = HistoricalRecords(table_name="task_history")

    class Meta:
        db_table = "task"

    @property
    def duration(self):
        return (
            self.setup_time
            + (self.run_time_per_unit * self.quantity)
            + self.teardown_time
        )
