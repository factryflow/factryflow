# Create your models here.
from common.models import BaseModelWithExtras

from django.core.exceptions import ValidationError
from django.db import models, transaction
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
    manual_priority = models.PositiveIntegerField(null=True, blank=True)
    planned_start_datetime = models.DateTimeField(null=True, blank=True)
    planned_end_datetime = models.DateTimeField(null=True, blank=True)

    priority = models.IntegerField(editable=False, null=True, default=None)

    # Special Fields
    order_field_name = "priority"
    history = HistoricalRecords(table_name="job_history")

    class Meta:
        db_table = "job"
        ordering = ("due_date",)

    class Meta(OrderedModelBase.Meta):
        ordering = ["priority", "due_date"]

    def update_priority(self, new_priority):
        if new_priority < 0:
            raise ValidationError("Priority must be greater or equal 0")
        self.to(new_priority)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.full_clean()

            # to update manual_priority if it's greater than the actual number of jobs
            all_jobs_count = Job.objects.exclude(job_status__in=["CM", "CN"]).count()
            if self.manual_priority:
                if self.pk is None:
                    if self.manual_priority > all_jobs_count:
                        self.manual_priority = all_jobs_count + 1
                else:
                    if self.manual_priority > all_jobs_count:
                        self.manual_priority = all_jobs_count

                self.priority = self.manual_priority

            super().save(*args, **kwargs)
            self.recalculate_priorities()

    def recalculate_priorities(self):
        """Recalculate priorities of all tasks, ensuring that jobs with a manual_priority retain that priority.
        If multiple jobs have the same manual_priority, reorder only those jobs based on due_date."""

        # Reset priorities for completed or cancelled jobs
        Job.objects.filter(job_status__in=["CM", "CN"]).update(priority=None)

        # Fetch active jobs, excluding completed or cancelled ones
        active_jobs = Job.objects.exclude(job_status__in=["CM", "CN"]).order_by(
            "due_date"
        )

        # Collect jobs by manual_priority to handle duplicates
        priority_to_jobs = {}
        for job in active_jobs:
            if job.manual_priority is not None:
                priority_to_jobs.setdefault(job.manual_priority, []).append(job)

        # Assign priorities: keep single instances with their manual_priority; resolve conflicts by due_date
        resolved_priorities = {}
        used_priorities = (
            set()
        )  # Track priorities already firmly assigned to avoid clashes

        # Process each manual_priority group
        for priority, jobs in priority_to_jobs.items():
            if len(jobs) == 1:
                # only one job with this manual_priority, assign it directly
                resolved_priorities[jobs[0].id] = priority
                used_priorities.add(priority)
            else:
                # Multiple jobs with the same manual_priority, sort by due_date and reassign
                sorted_jobs = sorted(jobs, key=lambda x: x.due_date)
                for index, job in enumerate(sorted_jobs):
                    if index == 0:
                        resolved_priorities[job.id] = (
                            priority  # First job retains the manual_priority
                        )
                    else:
                        # Find the next available priority that does not clash with other manual priorities
                        while priority in used_priorities:
                            priority += 1

                        resolved_priorities[job.id] = priority
                        Job.objects.filter(id=job.id).update(manual_priority=priority)
                        used_priorities.add(priority)

        # Assign priorities to jobs without a manual_priority, skipping used priorities
        next_priority = 1
        for job in active_jobs:
            if job.id not in resolved_priorities:
                # Ensure the assigned priority hasn't been used yet
                while next_priority in used_priorities:
                    next_priority += 1
                resolved_priorities[job.id] = next_priority
                used_priorities.add(next_priority)
                next_priority += 1

        # Update the database with the new priorities
        for job_id, priority in resolved_priorities.items():
            Job.objects.filter(id=job_id).update(priority=priority)

    def __str__(self):
        return self.name
