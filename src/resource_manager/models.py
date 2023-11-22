# Create your models here.
from django.db import models
from simple_history.models import HistoricalRecords

from common.models import BaseModel
from resource_calendar.models import WeeklyShiftTemplate


class Resource(BaseModel):
    name = models.CharField(max_length=100)

    history = HistoricalRecords(table_name="resource_history")

    # foreign keys
    weekly_shift_template = models.ForeignKey(
        WeeklyShiftTemplate,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="resources",
    )
    resource_groups = models.ManyToManyField("ResourceGroup", related_name="resources")

    class Meta:
        db_table = "resource"


class ResourceGroup(BaseModel):
    name = models.CharField(max_length=100)

    history = HistoricalRecords(table_name="resource_group_history")

    class Meta:
        db_table = "resource_group"
        db_table = "resource_group"
