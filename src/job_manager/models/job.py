# Create your models here.
from common.models import BaseModelWithExtras

#
from django.core.exceptions import ValidationError
from django.db import models
from ordered_model.models import OrderedModelBase
from simple_history.models import HistoricalRecords


class JobType(BaseModelWithExtras):
    name = models.CharField(max_length=150)

    history = HistoricalRecords(table_name="job_type_history")

    class Meta:
        db_table = "job_type"


class JobStatusChoices(models.TextChoices):
    NOT_PLANNED = "NP", "Not Planned"
    IN_PROGRESS = "IP", "In Progress"
    COMPLETED = "CM", "Completed"
    CANCELLED = "CN", "Cancelled"
    # TODO ON_HOLD = 'OH', 'On Hold'


class Job(BaseModelWithExtras, OrderedModelBase):
    # Core fields
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    customer = models.CharField(max_length=250, blank=True)
    due_date = models.DateField()
    job_status = models.CharField(
        max_length=2,
        choices=JobStatusChoices.choices,
        default=JobStatusChoices.NOT_PLANNED,
    )

    # Relationship fields
    job_type = models.ForeignKey(JobType, on_delete=models.DO_NOTHING)
    dependencies = models.ManyToManyField("Dependency", related_name="jobs")

    # Utility fields
    priority = models.PositiveIntegerField(db_index=True, editable=False)
    planned_start_datetime = models.DateTimeField(null=True, blank=True)
    planned_end_datetime = models.DateTimeField(null=True, blank=True)

    # Special Fields
    order_field_name = "priority"
    history = HistoricalRecords(table_name="job_history")

    class Meta:
        db_table = "job"
        ordering = ("priority",)

    def update_priority(self, new_priority):
        if new_priority < 0:
            raise ValidationError("Priority must be greater or equal 0")
        self.to(new_priority)
