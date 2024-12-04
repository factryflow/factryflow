from common.models import BaseModelWithExtras, BaseCriteria
from django.db import models
from job_manager.models import WorkCenter
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords


class AssigmentRule(BaseModelWithExtras, OrderedModel):
    """
    Represents a rule for assigning assignment constraints to tasks.
    """

    name = models.CharField(max_length=150)
    work_center = models.ForeignKey(WorkCenter, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    history = HistoricalRecords(table_name="assigment_rule_history")

    order_with_respect_to = "work_center"

    class Meta(OrderedModel.Meta):
        db_table = "assigment_rule"

    def __str__(self):
        return self.name


class AssigmentRuleCriteria(BaseCriteria):
    """
    To assign constraints to tasks, we need to be able to filter tasks by their fields.
    This model represents the criteria for filtering tasks.
    """

    id = models.AutoField(primary_key=True)
    assigment_rule = models.ForeignKey(
        AssigmentRule, on_delete=models.CASCADE, related_name="criteria"
    )

    history = HistoricalRecords(table_name="assigment_rule_criteria_history")

    class Meta:
        db_table = "assigment_rule_criteria"
