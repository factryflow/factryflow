from common.models import BaseModelWithExtras
from django.db import models
from simple_history.models import HistoricalRecords


class DependencyType(BaseModelWithExtras):
    name = models.CharField(max_length=150)

    history = HistoricalRecords(table_name="dependency_type_history")

    class Meta:
        db_table = "dependency_type"

    def __str__(self):
        return self.name


class DependencyStatusChoices(models.TextChoices):
    PENDING = "PD", "Pending"
    IN_PROGRESS = "IP", "In Progress"
    ON_HOLD = "OH", "On Hold"
    RESOLVED = "RS", "Resolved"
    CANCELLED = "CN", "Cancelled"

    @classmethod
    def to_dict(cls):
        """
        Convert the DependencyStatusChoices class into a dictionary.

        Returns:
        - Dictionary where choice values are keys and choice descriptions are values.
        """
        return {choice[0]: choice[1] for choice in cls.choices}


class Dependency(BaseModelWithExtras):
    name = models.CharField(max_length=150)
    expected_close_datetime = models.DateTimeField(blank=True, null=True)
    actual_close_datetime = models.DateTimeField(blank=True, null=True)
    dependency_type = models.ForeignKey(DependencyType, on_delete=models.DO_NOTHING)
    dependency_status = models.CharField(
        max_length=2,
        choices=DependencyStatusChoices.choices,
        default=DependencyStatusChoices.PENDING,
    )

    history = HistoricalRecords(table_name="dependency_history")

    class Meta:
        db_table = "dependency"

    def __str__(self):
        return self.name
