from common.models import BaseModelWithExtras
from django.db import models
from job_manager.models import WorkCenter
from simple_history.models import HistoricalRecords

from microbatching.models.microbatch_rule import MicrobatchRule


class MicrobatchFlow(BaseModelWithExtras):
    name = models.CharField(max_length=150)
    description = models.TextField()
    work_center = models.ForeignKey(WorkCenter, on_delete=models.CASCADE)
    start_rule = models.ForeignKey(
        MicrobatchRule, on_delete=models.CASCADE, related_name="flow_start_rule"
    )
    end_rule = models.ForeignKey(
        MicrobatchRule, on_delete=models.CASCADE, related_name="flow_end_rule"
    )
    min_flow_length = models.PositiveIntegerField()
    max_flow_length = models.PositiveIntegerField()

    history = HistoricalRecords(table_name="microbatch_flow_history")

    class Meta:
        db_table = "microbatch_flows"

    def __str__(self):
        return self.name
