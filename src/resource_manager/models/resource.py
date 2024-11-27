# Create your models here.
from common.models import BaseModelWithExtras
from django.conf import settings
from django.db import models
from resource_calendar.models import WeeklyShiftTemplate
from simple_history.models import HistoricalRecords


# -----------------------------------------------------------------------------
# Resource Type Choices
# -----------------------------------------------------------------------------


class ResourceTypeChoices(models.TextChoices):
    MACHINE = "Machine", "Machine"
    OPERATOR = "Operator", "Operator"

    @classmethod
    def to_dict(cls):
        """
        Convert the RESOURCE_TYPES class into a dictionary.

        Returns:
        - Dictionary where choice values are keys and choice descriptions are values.
        """
        return {choice[0]: choice[1] for choice in cls.choices}


# -----------------------------------------------------------------------------
# Resource
# -----------------------------------------------------------------------------


class Resource(BaseModelWithExtras):
    """
    The Resource model represents a resource that can be either a machine or an operator.
    Each resource has a name and a type, and can be associated with a weekly shift template.
    A resource can be part of multiple work units and resource pools, and can be operated by multiple users.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    resource_type = models.CharField(
        max_length=9,
        choices=ResourceTypeChoices.choices,
        default=ResourceTypeChoices.OPERATOR,
    )
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
    # resource_pools = models.ManyToManyField("ResourceGroup", related_name="resources")
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="operators", blank=True
    )

    class Meta:
        db_table = "resource"

    # @property
    # def resource_pool_id_list(self):
    #     return list(self.resource_pools.values_list("id", flat=True))

    def __str__(self):
        return self.name
