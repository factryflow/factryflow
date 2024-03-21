from common.models import BaseModel, BaseModelWithExtras
from django.core.exceptions import ValidationError
from django.db import models
from job_manager.models import Task, WorkCenter
from resource_manager.models import Resource, ResourcePool, WorkUnit

# Create your models here.


class TaskResourceAssigment(BaseModel):
    
    """
    Represents the assignment of resources to tasks.
    """

    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    # resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING)
    assigment_rule = models.ForeignKey(
        "AssigmentRule", on_delete=models.DO_NOTHING, blank=True, null=True
    )
    resource_pool = models.ManyToManyField(ResourcePool, blank=True)
    resource_count = models.PositiveIntegerField(default=1)
    use_all_resources = models.BooleanField(default=False)

    class Meta:
        db_table = "task_resource_assigment"

    


class AssigmentRule(BaseModelWithExtras):
    """
    Represents a rule for assigning assignment constraints to tasks.
    """

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    work_center = models.ForeignKey(WorkCenter, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "assigment_rule"

    def __str__(self):
        return self.name
    


class Operator(models.TextChoices):
    EQUALS = "equals", "Equals"
    CONTAINS = "contains", "Contains"
    STARTS_WITH = "starts_with", "Starts With"
    ENDS_WITH = "ends_with", "Ends With"
    GREATER_THAN = "gt", "Greater Than"
    LESS_THAN = "lt", "Less Than"


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

    class Meta:
        db_table = "assigment_rule_criteria"


class AssignmentConstraint(BaseModel):
    """
    Represents the constraints for assigning resources to tasks, such as resource pool or individual resources.
    Can be applied to each task to get dynamic assignemnts.
    """

    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        Task,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="constraints",
    )
    assignment_rule = models.ForeignKey(
        AssigmentRule,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="constraints",
    )
    resource_pool = models.ForeignKey(
        ResourcePool,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="constraints",
    )
    resources = models.ManyToManyField(Resource, blank=True, related_name="constraints")
    work_units = models.ManyToManyField(
        WorkUnit, blank=True, related_name="constraints"
    )
    required_units = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_direct = models.BooleanField(default=True)

    class Meta:
        db_table = "assignment_constraint"

    @property
    def is_template(self):
        return self.task is None

    @property
    def resource_id_list(self):
        return list(self.resources.values_list("id", flat=True))

    @property
    def work_unit_id_list(self):
        return list(self.work_units.values_list("id", flat=True))

    def clean(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        resource_pool_set = self.resource_pool_id is not None
        resources_set = self.resources is not None
        work_units_set = self.work_units is not None

        if resource_pool_set and (resources_set or work_units_set):
            raise ValidationError(
                "You cannot set both resource_pool and resources or work_units. Choose one."
            )
        elif not resource_pool_set and not (resources_set or work_units_set):
            raise ValidationError(
                "You must set either resource_pool or resources or work_units."
            )

        # ensure that either task or assignment_rule is set
        if not (self.task) and not (self.assignment_rule):
            raise ValidationError("task or assignment_rule must be set.")

        if self.is_direct and self.assignment_rule:
            raise ValidationError(
                "Direct assignment constraints cannot have assignment rules."
            )
