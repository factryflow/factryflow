from django.contrib.contenttypes.models import ContentType

from microbatching.models.microbatch_rule import (
    MicrobatchRule,
    MicrobatchRuleTaskMatch,
)
from job_manager.models import Task
from common.models import NestedCriteriaGroup
from common.utils.criteria import build_nested_query


def create_microbatch_rule_matches(tasks) -> list:
    result = {}

    try:
        matching_task_count = 0

        for task in tasks:
            # check if task is already matched with other rules
            # get all microbatch rules
            microbatch_rules = MicrobatchRule.objects.filter(is_active=True)

            if microbatch_rules:
                for rule in microbatch_rules:
                    # get the root NestedCriteriaGroup for the rule
                    try:
                        root_group = NestedCriteriaGroup.objects.get(
                            content_type=ContentType.objects.get_for_model(
                                MicrobatchRule
                            ),
                            object_id=rule.id,
                            parent_group=None,
                        )
                    except NestedCriteriaGroup.DoesNotExist:
                        continue

                    # # build a nested query for the root group
                    query = build_nested_query(root_group)

                    # check if the task matches the query
                    if query and Task.objects.filter(query, id=task.id).exists():
                        criteria_match = True
                        matching_task_count += 1
                    else:
                        criteria_match = False

                    if criteria_match:
                        is_rule_applied = True

                        task_rule_instance = MicrobatchRuleTaskMatch.objects.filter(
                            task=task, microbatch_rule=rule
                        )
                        if task_rule_instance.exists():
                            instance = task_rule_instance.first()
                            instance.is_applied = is_rule_applied
                            instance.save()

                        else:
                            # if criteria match store it in the TaskRuleAssignment model
                            task_rule_instance = MicrobatchRuleTaskMatch.objects.create(
                                task=task,
                                microbatch_rule=rule,
                                is_applied=is_rule_applied,
                            )
                            task_rule_instance.save()

                    else:
                        # if not criteria match, delete the TaskRuleAssignment model instance if exists
                        task_rule_microbatch = MicrobatchRuleTaskMatch.objects.filter(
                            task=task, microbatch_rule=rule
                        )
                        if task_rule_microbatch.exists():
                            task_rule_microbatch.delete()

        result["message"] = f"Matched {matching_task_count} tasks with microbatch rules"
        result["status"] = "success"

        return result
    except Exception as e:
        result["message"] = str(e)
        result["status"] = "error"
        return result
