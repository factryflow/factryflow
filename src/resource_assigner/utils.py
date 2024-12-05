from django.db import transaction
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from job_manager.models import Task
from resource_assigner.models import (
    AssigmentRule,
    TaskRuleAssignment,
)
from common.models import NestedCriteriaGroup
from common.utils.criteria import build_nested_query


@transaction.atomic
def get_matching_assignment_rules_with_tasks(tasks) -> list:
    """
    Matches tasks with assignment rules based on nested criteria and updates TaskRuleAssignment.
    """
    result = {}

    try:
        matching_task_count = 0

        for task in tasks:
            # get all active assignment rules for the task's work center
            assignment_rules = AssigmentRule.objects.filter(
                work_center=task.work_center, is_active=True
            ).order_by("order")

            if assignment_rules:
                for rule in assignment_rules:
                    # get the root NestedCriteriaGroup for the rule
                    try:
                        root_group = NestedCriteriaGroup.objects.filter(
                            content_type=ContentType.objects.get_for_model(
                                AssigmentRule
                            ),
                            object_id=rule.id,
                            parent_group=None,
                        )
                    except NestedCriteriaGroup.DoesNotExist:
                        continue

                    # build a nested query for the root group
                    query = Q()
                    for group in root_group:
                        # multiple parent groups for a rule
                        group_query = build_nested_query(group)
                        if group_query:
                            query &= group_query

                    # check if the task matches the query
                    if query and Task.objects.filter(query, id=task.id).exists():
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
