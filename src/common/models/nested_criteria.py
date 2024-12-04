from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords

from .base import BaseModel


class Operator(models.TextChoices):
    EQUALS = "equals", "Equals"
    NOT_EQUALS = "not_equals", "Not Equals"
    CONTAINS = "contains", "Contains"
    STARTS_WITH = "starts_with", "Starts With"
    ENDS_WITH = "ends_with", "Ends With"
    GREATER_THAN = "gt", "Greater Than"
    LESS_THAN = "lt", "Less Than"
    IN_BETWEEN = "ib", "In Between"


class LogicalOperator(models.TextChoices):
    AND = "AND", "AND"
    OR = "OR", "OR"


class BaseCriteria(BaseModel):
    """
    Abstract base model for criteria to be used by both AssignmentRuleCriteria and MicrobatchRuleCriteria.
    """

    field = models.CharField(max_length=100)
    operator = models.CharField(
        max_length=20, choices=Operator.choices, default=Operator.EQUALS
    )
    value = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        abstract = True


class NestedCriteriaGroup(BaseModel):
    """
    Groups criteria with a logical operator (AND/OR). Can be linked to either an AssignmentRule or MicrobatchRule.
    """

    # Generic relation to either AssignmentRule or MicrobatchRule
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_rule = GenericForeignKey("content_type", "object_id")

    operator = models.CharField(
        max_length=3, choices=LogicalOperator.choices, default=LogicalOperator.AND
    )

    # recursive relationship to self for nested groups within groups (if any)
    parent_group = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="nested_groups",
    )

    history = HistoricalRecords(table_name="nested_criteria_group_history")

    class Meta:
        db_table = "nested_criteria_group"

    def clean(self):
        # Ensure that the rule link is valid
        if not self.content_type or not self.object_id:
            raise ValidationError(
                "You must link either an assignment rule or a microbatch rule."
            )

    def __str__(self):
        if self.related_rule:
            return f"Group for {str(self.related_rule)}"
        return "Nested Criteria Group"


class NestedCriteria(BaseModel):
    """
    Represents individual criteria or nested groups in a NestedCriteriaGroup.
    """

    group = models.ForeignKey(
        NestedCriteriaGroup, on_delete=models.CASCADE, related_name="nested_group"
    )

    # Generic relation to either AssignmentRuleCriteria or MicrobatchRuleCriteria
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_criteria = GenericForeignKey("content_type", "object_id")

    history = HistoricalRecords(table_name="nested_criteria_history")

    class Meta:
        db_table = "nested_criteria"

    def __str__(self):
        if self.related_criteria:
            return f"Criteria: {str(self.related_criteria)} for group {str(self.group)}"
        return "Nested Criteria"
