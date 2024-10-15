from common.models import BaseModel, BaseModelWithExtras, Operator
from django.core.exceptions import ValidationError
from django.db import models
from job_manager.models import Task, WorkCenter
from ordered_model.models import OrderedModel
from resource_manager.models import Resource, ResourceGroup
from simple_history.models import HistoricalRecords


class TaskResourceAssigment(BaseModel):
    """
    Represents the assignment of resources to tasks.
    """

    task = models.OneToOneField(Task, on_delete=models.DO_NOTHING)
    resources = models.ManyToManyField(
        Resource, blank=True, related_name="task_resource_assignments"
    )

    history = HistoricalRecords(table_name="task_resource_assigment_history")

    class Meta:
        db_table = "task_resource_assigment"

    def __str__(self):
        return f"{self.task.name}"


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


class AssigmentRuleCriteria(BaseModel):
    """
    To assign constraints to tasks, we need to be able to filter tasks by their fields.
    This model represents the criteria for filtering tasks.
    """

    id = models.AutoField(primary_key=True)
    assigment_rule = models.ForeignKey(
        AssigmentRule, on_delete=models.CASCADE, related_name="criteria"
    )
    field = models.CharField(max_length=100)
    operator = models.CharField(
        max_length=20, choices=Operator.choices, default=Operator.EQUALS
    )
    value = models.CharField(max_length=254, blank=True, null=True)

    history = HistoricalRecords(table_name="assigment_rule_criteria_history")

    class Meta:
        db_table = "assigment_rule_criteria"


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
        on_delete=models.DO_NOTHING,
    )
    assignment_rule = models.OneToOneField(
        AssigmentRule,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )
    resource_group = models.ForeignKey(
        ResourceGroup,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="constraints",
    )
    resources = models.ManyToManyField(Resource, blank=True, related_name="constraints")
    resource_count = models.PositiveIntegerField(default=1)
    use_all_resources = models.BooleanField(default=False)

    history = HistoricalRecords(table_name="assignment_constraint_history")

    class Meta:
        db_table = "assignment_constraint"

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
