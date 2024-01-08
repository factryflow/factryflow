from django.db import models
from job_manager.models import Task, TaskStatusChoices
from resource_manager.models import Resource

from operator_view.models.issue import Issue


class InProgressOrCompletedManager(models.Manager):
    """
    This manager returns all tasks that are in progress or completed.
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                task_status__in=[
                    TaskStatusChoices.IN_PROGRESS,
                    TaskStatusChoices.COMPLETED,
                ]
            )
        )


class OperatorViewTask(Task):
    # Core fields
    thumbnail_url = models.URLField(max_length=255, blank=True, null=True)
    issue = models.ForeignKey(
        Issue, on_delete=models.DO_NOTHING, related_name="issues", blank=True, null=True
    )
    assigned_resource = models.ManyToManyField(
        Resource,
        related_name="assigned_resources",
        blank=True,
    )

    objects = models.Manager()  # The default manager
    in_progress_or_completed = InProgressOrCompletedManager()  # Custom manager

    class Meta:
        db_table = "operator_view_task"

    def update_issue_status(self, new_status):
        # TODO: Implementing "update" action for tags
        pass
