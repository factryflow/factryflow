from common.models import BaseCriteria, BaseModel, BaseModelWithExtras
from django.core.exceptions import ValidationError
from django.db import models
from job_manager.models.task import Task
from simple_history.models import HistoricalRecords


class MicrobatchRule(BaseModelWithExtras):
    """
    This groups tasks based on a set of criteria for microbatching.
    The tasks in a MicrobatchRule are then processed in a MicrobatchFlow.
    """

    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    history = HistoricalRecords(table_name="microbatch_rule_history")

    class Meta:
        db_table = "microbatch_rule"

    def __str__(self):
        return self.name


class MicrobatchRuleCriteria(BaseCriteria):
    """
    To assign microbatch rules to tasks, we need to be able to filter tasks by their fields.
    This model represents the criteria for filtering tasks.
    """

    id = models.AutoField(primary_key=True)
    microbatch_rule = models.ForeignKey(
        MicrobatchRule, on_delete=models.CASCADE, related_name="criteria"
    )

    history = HistoricalRecords(table_name="microbatch_rule_criteria_history")

    class Meta:
        db_table = "microbatch_rule_criteria"


class MicrobatchRuleTaskMatch(BaseModel):
    """
    Represents the microbatch rules to tasks.
    one task can match with multiple rules.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    microbatch_rule = models.ForeignKey(MicrobatchRule, on_delete=models.CASCADE)
    is_applied = models.BooleanField(default=False)

    history = HistoricalRecords(table_name="microbatch_rule_task_match_history")

    class Meta:
        db_table = "microbatch_rule_task_match"
        constraints = [
            models.UniqueConstraint(
                fields=["task", "microbatch_rule"], name="unique_task_microbatch_rule"
            )
        ]

    def __str__(self):
        return f"{self.task} - {self.microbatch_rule}"

    def clean(self, *args, **kwargs):
        # ensure that either task or microbatch_rule is set
        if not (self.task) and not (self.microbatch_rule):
            raise ValidationError("task or microbatch_rule must be set.")
