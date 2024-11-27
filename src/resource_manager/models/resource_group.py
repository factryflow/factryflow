# Create your models here.
from common.models import BaseModelWithExtras
from django.db import models
from simple_history.models import HistoricalRecords

from .resource import Resource


# -----------------------------------------------------------------------------
# Resource Group
# -----------------------------------------------------------------------------


class ResourceGroup(BaseModelWithExtras):
    """
    The ResourceGroup model represents a collection of resources.
    Each resource group has a name.
    A resource group can have a parent resource group, allowing for a hierarchy of resource group.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    resources = models.ManyToManyField(Resource, related_name="related_resources")
    history = HistoricalRecords(table_name="resource_grp_history")

    class Meta:
        db_table = "resource_pool"

    @property
    def resource_id_list(self):
        return list(self.resources.values_list("id", flat=True))

    def __str__(self):
        return self.name
