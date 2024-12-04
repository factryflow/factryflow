from django.db import transaction
from django.db.models import Q

from resource_assigner.models import (
    AssigmentRule,
    TaskRuleAssignment,
)
from common.models import NestedCriteriaGroup


def build_nested_query(group):
    """
    Builds a nested Q object for a given NestedCriteriaGroup.
    """
    query = Q()

    for nested_criteria in group.nested_group.all():
        if nested_criteria.related_criteria:
            # Handle individual criteria
            field = nested_criteria.related_criteria.field
            operator = nested_criteria.related_criteria.operator
            value = nested_criteria.related_criteria.value

            # Map operator to Q filters
            operator_mapping = {
                "equals": "",
                "not_equals": "__ne",
                "contains": "__icontains",
                "starts_with": "__istartswith",
                "ends_with": "__iendswith",
                "gt": "__gt",
                "lt": "__lt",
                "ib": "__range",
            }

            filter_key = f"{field}{operator_mapping.get(operator, '')}"
            if operator == "ib":
                value_parts = value.split(",")  # Handle ranges as "start,end"
                query_part = Q(**{filter_key: (value_parts[0], value_parts[1])})
            else:
                query_part = Q(**{filter_key: value})

            # Combine based on logical operator
            if group.operator == "AND":
                query &= query_part
            else:  # OR
                query |= query_part
        elif nested_criteria.group:
            # Handle nested groups
            nested_query = build_nested_query(nested_criteria.group)
            if group.operator == "AND":
                query &= nested_query
            else:
                query |= nested_query

    return query


@transaction.atomic
def get_matching_assignment_rules_with_tasks(tasks) -> list:
    """
    Matches tasks with assignment rules based on nested criteria and updates TaskRuleAssignment.
    """
    result = {}

    try:
        matching_task_count = 0

        for task in tasks:
            # Get all active assignment rules for the task's work center
            assignment_rules = AssigmentRule.objects.filter(
                work_center=task.work_center, is_active=True
            ).order_by("order")

            if assignment_rules:
                for rule in assignment_rules:
                    # Get the root NestedCriteriaGroup for the rule
                    try:
                        root_group = NestedCriteriaGroup.objects.get(
                            related_rule=rule, parent_group__isnull=True
                        )
                    except NestedCriteriaGroup.DoesNotExist:
                        continue

                    # Build a nested query for the root group
                    query = build_nested_query(root_group)

                    # Check if the task matches the query
                    if (
                        query
                        and TaskRuleAssignment.objects.filter(query, task=task).exists()
                    ):
                        criteria_match = True
                        matching_task_count += 1
                    else:
                        criteria_match = False

                    if criteria_match:
                        is_rule_applied = True
                        task_instance = TaskRuleAssignment.objects.filter(
                            task=task, is_applied=True
                        ).exclude(assigment_rule=rule)

                        if task_instance.exists():
                            existing_rule_order = (
                                task_instance.first().assigment_rule.order
                            )

                            if existing_rule_order > rule.order:
                                task_instance.first().is_applied = False
                                task_instance.first().save()

                            if existing_rule_order < rule.order:
                                is_rule_applied = False

                        task_rule_instance = TaskRuleAssignment.objects.filter(
                            task=task, assigment_rule=rule
                        )
                        if task_rule_instance.exists():
                            instance = task_rule_instance.first()
                            instance.is_applied = is_rule_applied
                            instance.save()
                        else:
                            # If criteria match, store it in the TaskRuleAssignment model
                            TaskRuleAssignment.objects.create(
                                task=task,
                                assigment_rule=rule,
                                is_applied=is_rule_applied,
                            )
                    else:
                        # If no criteria match, delete any existing TaskRuleAssignment
                        TaskRuleAssignment.objects.filter(
                            task=task, assigment_rule=rule
                        ).delete()

        result["message"] = f"Matched {matching_task_count} tasks with assignment rules"
        result["status"] = "success"

        return result
    except Exception as e:
        result["message"] = str(e)
        result["status"] = "error"
        return result
