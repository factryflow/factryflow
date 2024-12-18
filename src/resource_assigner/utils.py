from common.models import NestedCriteriaGroup
from common.utils.criteria import build_nested_query
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from job_manager.models import Task

from resource_assigner.models import (
    AssigmentRule,
    TaskRuleAssignment,
)


@transaction.atomic
def get_matching_assignment_rules_with_tasks() -> list:
    """
    Matches tasks with assignment rules based on nested criteria and updates TaskRuleAssignment.
    """
    result = {}

    try:
        matching_task_count = 0

        TaskRuleAssignment.objects.all().delete()

        # Get all active assignment rules
        assignment_rules = AssigmentRule.objects.filter(is_active=True).order_by(
            "order"
        )

        if assignment_rules:
            applied_matches = []
            applied_count = 0
            for rule in assignment_rules:
                # Get the root NestedCriteriaGroup for the rule
                try:
                    root_group = NestedCriteriaGroup.objects.filter(
                        content_type=ContentType.objects.get_for_model(AssigmentRule),
                        object_id=rule.id,
                        parent_group=None,
                    )
                except NestedCriteriaGroup.DoesNotExist:
                    continue

                # Build a nested query for the root group
                query = Q()
                for group in root_group:
                    # Multiple parent groups for a rule
                    group_query = build_nested_query(group)
                    if group_query:
                        query &= group_query

                # Check if any task matches the query
                matching_tasks = Task.objects.filter(query).iterator()
                matching_task_count += Task.objects.filter(query).count()

                task_rule_assignments = []
                for task in matching_tasks:
                    if task.id in applied_matches:
                        applied_rule = False
                    else:
                        applied_matches.append(task.id)
                        applied_rule = True
                        applied_count += 1

                    task_rule_assignment = TaskRuleAssignment(
                        task=task,
                        assigment_rule=rule,
                        is_applied=applied_rule,
                    )

                    task_rule_assignments.append(task_rule_assignment)

                    # Bulk create TaskRuleAssignment instances in batches
                    if len(task_rule_assignments) >= 1000:
                        TaskRuleAssignment.objects.bulk_create(task_rule_assignments)
                        task_rule_assignments = []

                # Create any remaining TaskRuleAssignment instances
                if task_rule_assignments:
                    TaskRuleAssignment.objects.bulk_create(task_rule_assignments)

        result["message"] = (
            f"Created {matching_task_count} task matches with assignment rules"
        )
        result["status"] = "success"
        return result
    except Exception as e:
        result["message"] = str(e)
        result["status"] = "error"
        return result
