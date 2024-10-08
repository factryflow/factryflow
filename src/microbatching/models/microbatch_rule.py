from common.models import BaseModel, BaseModelWithExtras
from django.db import models
from job_manager.models import WorkCenter
from simple_history.models import HistoricalRecords


class Operator(models.TextChoices):
    EQUALS = "equals", "Equals"
    CONTAINS = "contains", "Contains"
    STARTS_WITH = "starts_with", "Starts With"
    ENDS_WITH = "ends_with", "Ends With"
    GREATER_THAN = "gt", "Greater Than"
    LESS_THAN = "lt", "Less Than"


class MicrobatchRule(BaseModelWithExtras):
    """
    This groups tasks based on a set of criteria for microbatching.
    The tasks in a MicrobatchRule are then processed in a MicrobatchFlow.
    """

    item_name = models.CharField(max_length=150)
    work_center = models.ForeignKey(WorkCenter, on_delete=models.CASCADE)
    batch_size = models.IntegerField()

    history = HistoricalRecords(table_name="microbatch_rule_history")

    class Meta:
        db_table = "microbatch_rule"

    def __str__(self):
        return f"{self.item_name} - {self.work_center}"


class MicrobatchRuleCriteria(BaseModel):
    """
    To assign microbatch rules to tasks, we need to be able to filter tasks by their fields.
    This model represents the criteria for filtering tasks.
    """

    id = models.AutoField(primary_key=True)
    microbatch_rule = models.ForeignKey(
        MicrobatchRule, on_delete=models.CASCADE, related_name="criteria"
    )
    field = models.CharField(max_length=100)
    operator = models.CharField(
        max_length=20, choices=Operator.choices, default=Operator.EQUALS
    )
    value = models.CharField(max_length=254, blank=True, null=True)

    history = HistoricalRecords(table_name="microbatch_rule_criteria_history")

    class Meta:
        db_table = "microbatch_rule_criteria"
