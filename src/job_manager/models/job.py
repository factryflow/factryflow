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

    def __str__(self):
        return self.name


class JobStatusChoices(models.TextChoices):
    NOT_PLANNED = "NP", "Not Planned"
    IN_PROGRESS = "IP", "In Progress"
    COMPLETED = "CM", "Completed"
    CANCELLED = "CN", "Cancelled"
    # TODO ON_HOLD = 'OH', 'On Hold'

    @classmethod
    def to_dict(cls):
        """
        Convert the JobStatusChoices class into a dictionary.

        Returns:
        - Dictionary where choice values are keys and choice descriptions are values.
        """
        return {choice[0]: choice[1] for choice in cls.choices}


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
    dependencies = models.ManyToManyField("Dependency", related_name="jobs", blank=True)

    # Utility fields
    priority = models.PositiveIntegerField(db_index=True)
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

    def __str__(self):
        return self.name

    def consolidate_start_end_dates(self):
        """Sets the planned start and end dates for the Job based on the earliest
        start date and latest end date from the child tasks (if any).
        """
        if self.tasks.exists():
            start_dates = [
                task.planned_start_datetime
                for task in self.tasks.all()
                if task.planned_start_datetime
            ]
            end_dates = [
                task.planned_end_datetime
                for task in self.tasks.all()
                if task.planned_end_datetime
            ]

            if start_dates and end_dates:
                self.planned_start_datetime = min(start_dates)
                self.planned_end_datetime = max(end_dates)
                self.save()
