from common.models import BaseModel
from django.db import models
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager


class Issue(BaseModel):
    # Core fields
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True, null=True)
    issuer = models.CharField(max_length=150, blank=True, null=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)

    objects = models.Manager()  # Default manager
    tags = TaggableManager()  # Tag manager

    # Relationship fields
    task = models.ForeignKey(
        "OperatorViewTask",
        models.DO_NOTHING,
        related_name="tasks",
    )
    item = models.ForeignKey(
        "OperatorViewTask",
        models.DO_NOTHING,
        related_name="items",
    )

    # Special Fields
    history = HistoricalRecords(table_name="issue_history")

    class Meta:
        db_table = "issue"
