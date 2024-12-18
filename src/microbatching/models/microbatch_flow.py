from common.models import BaseModel, BaseModelWithExtras
from django.db import models
from job_manager.models.task import Task
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords

from microbatching.models.microbatch_rule import MicrobatchRule


class MicrobatchFlow(BaseModelWithExtras, OrderedModel):
    """Main model for determining the flow of tasks in a microbatch."""

    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    batch_size = models.IntegerField()
    start_rule = models.ForeignKey(
        MicrobatchRule, on_delete=models.CASCADE, related_name="flow_start_rule"
    )
    end_rule = models.ForeignKey(
        MicrobatchRule, on_delete=models.CASCADE, related_name="flow_end_rule"
    )
    min_flow_length = models.PositiveIntegerField(default=2)
    max_flow_length = models.PositiveIntegerField(default=3)

    history = HistoricalRecords(table_name="microbatch_flow_history")

    class Meta(OrderedModel.Meta):
        db_table = "microbatch_flows"

    def __str__(self):
        return self.name


class MicrobatchTaskFlow(BaseModel):
    """Stores a set of MicrobatchTasks that are derived from a MicrobatchFlow."""

    microbatch_flow = models.ForeignKey(
        MicrobatchFlow, on_delete=models.CASCADE, related_name="task_flows"
    )

    class Meta:
        db_table = "microbatch_task_flow"

    def __str__(self):
        task_flow_str = " -> ".join([n.task.name for n in self.flow_tasks.all()])
        return f"{self.id} - {self.microbatch_flow.name} - {task_flow_str}"

    @property
    def name(self):
        return " -> ".join([n.task.name for n in self.flow_tasks.all()])


class MicrobatchTask(BaseModel, OrderedModel):
    """Stores data on flows derived from Tasks and their matching MicrobatchRules."""

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    microbatch_task_flow = models.ForeignKey(
        MicrobatchTaskFlow, on_delete=models.CASCADE, related_name="flow_tasks"
    )

    history = HistoricalRecords(table_name="microbatch_task_flow_history")

    order_with_respect_to = "microbatch_task_flow"

    class Meta(OrderedModel.Meta):
        db_table = "microbatch_task"

    def __str__(self):
        flow = self.microbatch_task_flow
        return f"{flow.microbatch_flow.name} - {self.task.name} - {flow.id}"

    def __unicode__(self):
        flow = self.microbatch_task_flow
        return f"{flow.microbatch_flow.name} - {self.task.name} - {flow.id}"
