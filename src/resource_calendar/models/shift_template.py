from common.models import BaseModelWithExtras
from django.db import models
from simple_history.models import HistoricalRecords


# ------------------------------------------------------------------------------
# Weekly Shift Template Models
# ------------------------------------------------------------------------------


class WeeklyShiftTemplate(BaseModelWithExtras):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    history = HistoricalRecords(table_name="weekly_shift_template_history")

    class Meta:
        db_table = "weekly_shift_template"

    def __str__(self):
        return self.name
