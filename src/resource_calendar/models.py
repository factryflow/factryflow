from common.models import BaseModel, BaseModelWithExtras
from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords

# ------------------------------------------------------------------------------
# Weekly Shift Template Models
# ------------------------------------------------------------------------------


class WeeklyShiftTemplate(BaseModelWithExtras):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    weekly_shift_template_details = models.ManyToManyField(
        "WeeklyShiftTemplateDetail",
        related_name="weekly_shift_template",
        blank=True,
    )

    history = HistoricalRecords(table_name="weekly_shift_template_history")

    class Meta:
        db_table = "weekly_shift_template"

    def __str__(self):
        return self.name
    


class DaysOfWeek(models.TextChoices):
    MONDAY = "Monday", "Monday"
    TUESDAY = "Tuesday", "Tuesday"
    WEDNESDAY = "Wednesday", "Wednesday"
    THURSDAY = "Thursday", "Thursday"
    FRIDAY = "Friday", "Friday"
    SATURDAY = "Saturday", "Saturday"
    SUNDAY = "Sunday", "Sunday"



class WeeklyShiftTemplateDetail(BaseModel):
    day_of_week = models.TextField(choices=DaysOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    history = HistoricalRecords(table_name="weekly_shift_template_detail_history")

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")
        

    class Meta:
        indexes = [
            models.Index(
                fields=["day_of_week"],
            )
        ]
        unique_together = [
            ["day_of_week", "start_time", "end_time"]
        ]
        db_table = "weekly_shift_template_detail" 

    def __str__(self):
        return f"{self.day_of_week} {self.start_time} - {self.end_time}"                      


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
