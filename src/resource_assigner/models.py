from common.models import BaseModel
from django.core.exceptions import ValidationError
from django.db import models
from job_manager.models import Task, WorkCenter
from resource_manager.models import Resource, ResourceGroup

# Create your models here.


class TaskResourceAssigment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    resource_group = models.ForeignKey(ResourceGroup, on_delete=models.DO_NOTHING)
    resources = models.ManyToManyField(
        Resource, related_name="task_resource_assigments", blank=True, null=True
    )
    resource_count = models.IntegerField(blank=True, null=True)
    use_all_resources = models.BooleanField()
    is_direct = models.BooleanField()

    class Meta:
        db_table = "task_resource_assigment"

    def clean(self):
        if self.resources and self.resource_group.id != 1:
            raise ValidationError(
                "Resource group must be 'All Resources' if resources are selected"
            )

        # Check that only one of resources, resource_count, use_all_resources is set
        true_count = sum(
            [bool(self.resources), bool(self.resource_count), self.use_all_resources]
        )

        if true_count > 1:
            raise ValidationError(
                "Only one of resources, resource_count, use_all_resources can be set"
            )

        if true_count == 0:
            raise ValidationError(
                "One of resources, resource_count, use_all_resources must be set"
            )


class AssigmentRule(BaseModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    resource_group = models.ForeignKey(ResourceGroup, on_delete=models.DO_NOTHING)
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
