from common.models import BaseModelWithExtras
from django.db import models
from job_manager.models import WorkCenter
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords

from microbatching.models.microbatch_rule import MicrobatchRule


class MicrobatchFlow(BaseModelWithExtras):
    name = models.CharField(max_length=150)
    description = models.TextField()
    work_center = models.ForeignKey(WorkCenter, on_delete=models.CASCADE)

    history = HistoricalRecords(table_name="microbatch_flow_history")

    class Meta:
        db_table = "microbatch_flow"

    def __str__(self):
        return self.name


class MicrobatchFlowStep(BaseModelWithExtras, OrderedModel):
    name = models.CharField(max_length=150)
    description = models.TextField()
    size = models.IntegerField()
    microbatch_flow = models.ForeignKey(MicrobatchFlow, on_delete=models.CASCADE)
    predecessor_rule = models.ForeignKey(
        MicrobatchRule,
        on_delete=models.DO_NOTHING,
        related_name="predecessor_flow_steps",
    )
    current_rule = models.ForeignKey(
        MicrobatchRule, on_delete=models.DO_NOTHING, related_name="current_flow_steps"
    )

    order_with_respect_to = "microbatch_flow"

    history = HistoricalRecords(table_name="microbatch_flow_step_history")

    class Meta(OrderedModel.Meta):
        db_table = "microbatch_flow_step"

    def __str__(self):
        return self.name
