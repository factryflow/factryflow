# Create your models here.
from common.models import BaseModelWithExtras
from django.contrib.auth.models import User
from django.db import models
from resource_calendar.models import WeeklyShiftTemplate
from simple_history.models import HistoricalRecords


class Resource(BaseModelWithExtras):
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
    users = models.ManyToManyField(User, related_name="operators")

    class Meta:
        db_table = "resource"

    @property
    def resource_group_id_list(self):
        return list(self.resource_groups.values_list("id", flat=True))


class ResourceGroup(BaseModelWithExtras):
    name = models.CharField(max_length=100)

    history = HistoricalRecords(table_name="resource_group_history")

    class Meta:
        db_table = "resource_group"

    @property
    def resource_id_list(self):
        return list(self.resources.values_list("id", flat=True))
