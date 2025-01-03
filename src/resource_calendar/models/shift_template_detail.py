from common.models import BaseModelWithExtras
from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords

from .shift_template import WeeklyShiftTemplate

# ------------------------------------------------------------------------------
# Weekly Shift Template Detail Models
# ------------------------------------------------------------------------------


class DaysOfWeek(models.TextChoices):
    MONDAY = "Monday", "Monday"
    TUESDAY = "Tuesday", "Tuesday"
    WEDNESDAY = "Wednesday", "Wednesday"
    THURSDAY = "Thursday", "Thursday"
    FRIDAY = "Friday", "Friday"
    SATURDAY = "Saturday", "Saturday"
    SUNDAY = "Sunday", "Sunday"


class WeeklyShiftTemplateDetail(BaseModelWithExtras):
    weekly_shift_template = models.ForeignKey(
        WeeklyShiftTemplate,
        on_delete=models.CASCADE,
        related_name="weekly_shift_template_details",
    )
    day_of_week = models.TextField(choices=DaysOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    history = HistoricalRecords(table_name="weekly_shift_template_detail_history")

    class Meta:
        indexes = [
            models.Index(
                fields=["day_of_week"],
            )
        ]
        unique_together = [
            ["weekly_shift_template", "day_of_week", "start_time", "end_time"]
        ]
        db_table = "weekly_shift_template_detail"

    def __str__(self):
        return f"{self.day_of_week} {self.start_time} - {self.end_time}"

    def get_day_of_week_number(self):
        # get the number of day by self.day_of_week
        day_of_week = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        return day_of_week.index(self.day_of_week) + 1
