from common.models import BaseModel
from django.db import models
from job_manager.models.task import Task
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager


class Issue(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    # Core fields
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    # TODO: Integrate with Azure Storage instead of Django Storage.
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    # Relationship fields
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, related_name="issues")

    # Defining custom managers
    objects = models.Manager()  # Default manager.
    tags = TaggableManager()  # Tagging support.

    # Special fields
    history = HistoricalRecords(table_name="issue_history")

    class Meta:
        db_table = "task_issue"


class Comment(BaseModel):
    # Core fields
    body = models.TextField()

    # Relationship fields
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")

    # Special fields
    history = HistoricalRecords(table_name="comment_history")

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Comment by {self.created_by} on {self.issue}"
