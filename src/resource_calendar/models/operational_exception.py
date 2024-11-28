from common.models import BaseModelWithExtras
from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords

from .shift_template import WeeklyShiftTemplate


# ------------------------------------------------------------------------------
# Operational Exception Models
# ------------------------------------------------------------------------------


class OperationalExceptionType(BaseModelWithExtras):
    name = models.CharField(max_length=150)

    history = HistoricalRecords(table_name="operational_exception_type_history")

    class Meta:
        db_table = "operational_exception_type"

    def __str__(self):
        return self.name


# ------------------------------------------------------------------------------
# Operational Exception Models
# ------------------------------------------------------------------------------


class OperationalException(BaseModelWithExtras):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    # foreign keys
    operational_exception_type = models.ForeignKey(
        OperationalExceptionType,
        on_delete=models.DO_NOTHING,
    )
    weekly_shift_template = models.ForeignKey(
        WeeklyShiftTemplate, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    resource = models.ForeignKey(
        "resource_manager.Resource",
        on_delete=models.DO_NOTHING,
        related_name="operational_exceptions",
    )

    history = HistoricalRecords(table_name="operational_exception_history")

    def clean(self):
        if self.start_datetime > self.end_datetime:
            raise ValidationError("Start datetime must be before end datetime")

    class Meta:
        db_table = "operational_exception"
