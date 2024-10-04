from common.models import BaseModelWithExtras
from django.db import models
from job_manager.models import WorkCenter
from simple_history.models import HistoricalRecords


class MicrobatchRule(BaseModelWithExtras):
    item_name = models.CharField(max_length=150)
    work_center = models.ForeignKey(WorkCenter, on_delete=models.CASCADE)
    batch_size = models.IntegerField()

    history = HistoricalRecords(table_name="microbatch_rule_history")

    class Meta:
        db_table = "microbatch_rule"

    def __str__(self):
        return f"{self.item_name} - {self.work_center}"
