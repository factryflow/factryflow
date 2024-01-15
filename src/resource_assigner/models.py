from common.models import BaseModel
from django.core.exceptions import ValidationError
from django.db import models
from job_manager.models import Task, WorkCenter
from resource_manager.models import Resource, ResourcePool, WorkUnit

# Create your models here.


class TaskResourceAssigment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    resource_pool = models.ForeignKey(ResourcePool, on_delete=models.DO_NOTHING)
    resources = models.ManyToManyField(Resource, blank=True, related_name="assigments")
    work_units = models.ManyToManyField(WorkUnit, blank=True, related_name="assigments")
    units_required = models.PositiveIntegerField(default=1)
    is_direct = models.BooleanField(default=True)

    class Meta:
        db_table = "task_resource_assigment"

    def clean(self):
        true_count = sum(
            [self.resource_pool, bool(self.resources) and bool(self.work_units)]
        )

        if true_count > 1 or true_count == 0:
            raise ValidationError(
                "Either resource_pool or resources and work_units must be set"
            )


class AssigmentRule(BaseModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    resource_pool = models.ForeignKey(ResourcePool, on_delete=models.DO_NOTHING)
    work_center = models.ForeignKey(WorkCenter, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "assigment_rule"


class Operator(models.TextChoices):
    EQUALS = "equals", "Equals"
    CONTAINS = "contains", "Contains"
    STARTS_WITH = "starts_with", "Starts With"
    ENDS_WITH = "ends_with", "Ends With"
    GREATER_THAN = "gt", "Greater Than"
    LESS_THAN = "lt", "Less Than"


class AssigmentRuleCriteria(BaseModel):
    assigment_rule = models.ForeignKey(
        AssigmentRule, on_delete=models.CASCADE, related_name="criteria"
    )
    field = models.CharField(max_length=100)
    operator = models.CharField(
        max_length=20, choices=Operator.choices, default=Operator.EQUALS
    )
    value = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        db_table = "assigment_rule_criteria"
