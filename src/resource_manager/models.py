# Create your models here.
from common.models import BaseModelWithExtras
from django.contrib.auth.models import User
from django.db import models
from resource_calendar.models import WeeklyShiftTemplate
from simple_history.models import HistoricalRecords


class Resource(BaseModelWithExtras):
    """
    The Resource model represents a resource that can be either a machine or an operator.
    Each resource has a name and a type, and can be associated with a weekly shift template.
    A resource can be part of multiple work units and resource pools, and can be operated by multiple users.
    """

    RESOURCE_TYPES = [
        ("M", "Machine"),
        ("O", "Operator"),
    ]

    name = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=1, choices=RESOURCE_TYPES)
    history = HistoricalRecords(table_name="resource_history")

    # foreign keys
    weekly_shift_template = models.ForeignKey(
        WeeklyShiftTemplate,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="resources",
    )

    # many to many fields
    work_units = models.ManyToManyField("WorkUnit", related_name="resources")
    resource_pools = models.ManyToManyField("ResourcePool", related_name="resources")
    users = models.ManyToManyField(User, related_name="operators")

    class Meta:
        db_table = "resource"

    @property
    def resource_pool_id_list(self):
        return list(self.resource_pools.values_list("id", flat=True))

    @property
    def work_unit_id_list(self):
        return list(self.work_units.values_list("id", flat=True))


class WorkUnit(BaseModelWithExtras):
    """
    The WorkUnit model represents a team of resources.
    Each work unit has a name and can be associated with multiple resources and resource pools.
    """

    name = models.CharField(max_length=100)
    history = HistoricalRecords(table_name="work_unit_history")

    class Meta:
        db_table = "work_unit"

    @property
    def resource_id_list(self):
        return list(self.resources.values_list("id", flat=True))

    @property
    def resource_pool_id_list(self):
        return list(self.resource_pools.values_list("id", flat=True))


class ResourcePool(BaseModelWithExtras):
    """
    The ResourcePool model represents a collection of resources and work units.
    Each resource pool has a name and can be associated with multiple work units.
    A resource pool can have a parent resource pool, allowing for a hierarchy of resource pools.
    """

    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    work_units = models.ManyToManyField(WorkUnit, related_name="resource_pools")
    history = HistoricalRecords(table_name="resource_pool_history")

    class Meta:
        db_table = "resource_pool"

    @property
    def resource_id_list(self):
        return list(self.resources.values_list("id", flat=True))

    @property
    def work_unit_id_list(self):
        return list(self.work_units.values_list("id", flat=True))
