from common.models import BaseModel
from django.core.exceptions import ValidationError
from django.db import models
from job_manager.models import Task
from resource_manager.models import Resource, ResourceGroup
from simple_history.models import HistoricalRecords

from .rule_criteria import AssigmentRule


class AssignmentConstraint(BaseModel):
    """
    Represents the constraints for assigning resources to tasks, such as resource pool or individual resources.
    Can be applied to each task to get dynamic assignemnts.
    """

    id = models.AutoField(primary_key=True)
    task = models.OneToOneField(
        Task,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    assignment_rule = models.OneToOneField(
        AssigmentRule,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    resource_group = models.ForeignKey(
        ResourceGroup,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="constraints",
    )
    resources = models.ManyToManyField(Resource, blank=True, related_name="constraints")
    resource_count = models.PositiveIntegerField(default=1)
    use_all_resources = models.BooleanField(default=False)

    history = HistoricalRecords(table_name="assignment_constraint_history")

    class Meta:
        db_table = "assignment_constraint"

    def __str__(self):
        if self.task:
            return f"AssignmentConstraint for Task: {self.task.name}"
        elif self.assignment_rule:
            return (
                f"AssignmentConstraint for Assignment Rule: {self.assignment_rule.name}"
            )
        else:
            return "AssignmentConstraint with no associated Task or Assignment Rule"

    @property
    def is_template(self):
        return self.task is None

    @property
    def resource_id_list(self):
        return list(self.resources.values_list("id", flat=True))

    def clean(self, *args, **kwargs):
        # ensure that either task or assignment_rule is set
        if not (self.task) and not (self.assignment_rule):
            raise ValidationError("task or assignment_rule must be set.")
