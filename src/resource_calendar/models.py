from common.models import BaseModel
from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords

# ------------------------------------------------------------------------------
# Weekly Shift Template Models
# ------------------------------------------------------------------------------


class WeeklyShiftTemplate(BaseModel):
    name = models.CharField(max_length=150, blank=True, null=True)

    history = HistoricalRecords(table_name="weekly_shift_template_history")

    class Meta:
        db_table = "weekly_shift_template"


class WeeklyShiftTemplateDetail(BaseModel):
    day_of_week = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    weekly_shift_template = models.ForeignKey(
        WeeklyShiftTemplate,
        on_delete=models.CASCADE,
        related_name="weekly_shift_template_details",
    )

    history = HistoricalRecords(table_name="weekly_shift_template_detail_history")

    def clean(self):
        if self.day_of_week < 0 or self.day_of_week > 6:
            raise ValidationError("Day of week must be between 0 and 6")
        if self.start_time > self.end_time:
            raise ValidationError("Start time must be before end time")

    class Meta:
        db_table = "weekly_shift_template_detail"


# ------------------------------------------------------------------------------
# Operational Exception Models
# ------------------------------------------------------------------------------


class OperationalExceptionType(BaseModel):
    name = models.CharField(max_length=150)

    history = HistoricalRecords(table_name="operational_exception_type_history")

    class Meta:
        db_table = "operational_exception_type"


class OperationalException(BaseModel):
    external_id = models.CharField(max_length=250, blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

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
