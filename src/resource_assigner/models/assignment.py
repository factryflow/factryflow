from common.models import BaseModel
from django.core.exceptions import ValidationError
from django.db import models
from job_manager.models import Task
from resource_manager.models import Resource
from simple_history.models import HistoricalRecords

from .rule_criteria import AssigmentRule


class TaskResourceAssigment(BaseModel):
    """
    Represents the assignment of resources to tasks.
    """

    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    resources = models.ManyToManyField(
        Resource, blank=True, related_name="task_resource_assignments"
    )

    history = HistoricalRecords(table_name="task_resource_assigment_history")

    class Meta:
        db_table = "task_resource_assigment"

    def __str__(self):
        return f"{self.task.name}"


class TaskRuleAssignment(BaseModel):
    """
    Represents the assignment rules to tasks.
    one task can have multiple rules.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assigment_rule = models.ForeignKey(AssigmentRule, on_delete=models.CASCADE)
    is_applied = models.BooleanField(default=False)

    history = HistoricalRecords(table_name="task_rule_assignment_history")

    class Meta:
        db_table = "task_rule_assignment"
        constraints = [
            models.UniqueConstraint(
                fields=["task", "assigment_rule"], name="unique_task_assigment_rule"
            )
        ]

    def __str__(self):
        return f"{self.task} - {self.assigment_rule}"

    def clean(self, *args, **kwargs):
        # ensure that either task or assignment_rule is set
        if not (self.task) and not (self.assignment_rule):
            raise ValidationError("task or assignment_rule must be set.")
