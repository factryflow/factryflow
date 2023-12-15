from common.models import BaseModel
from django.db import models
from simple_history.models import HistoricalRecords


class DependencyType(BaseModel):
    name = models.CharField(max_length=150)

    history = HistoricalRecords(table_name="dependency_type_history")

    class Meta:
        db_table = "dependency_type"


class DependencyStatusChoices(models.TextChoices):
    PENDING = "PD", "Pending"
    IN_PROGRESS = "IP", "In Progress"
    ON_HOLD = "OH", "On Hold"
    RESOLVED = "RS", "Resolved"
    CANCELLED = "CN", "Cancelled"


class Dependency(BaseModel):
    name = models.CharField(max_length=150)
    external_id = models.CharField(max_length=180, blank=True)
    expected_close_datetime = models.DateTimeField(blank=True, null=True)
    actual_close_datetime = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)
    dependency_type = models.ForeignKey(DependencyType, on_delete=models.DO_NOTHING)
    dependency_status = models.CharField(
        max_length=2,
        choices=DependencyStatusChoices.choices,
        default=DependencyStatusChoices.PENDING,
    )

    history = HistoricalRecords(table_name="dependency_history")

    class Meta:
        db_table = "dependency"
