# Create your models here.
from common.models import BaseModel
from django.db import models
from resource_calendar.models import WeeklyShiftTemplate


class Resource(BaseModel):
    name = models.CharField(max_length=100)

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

    class Meta:
        db_table = "resource_group"
