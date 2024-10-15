from common.utils.services import check_criteria_match

from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    TaskRuleAssignment,
)


def get_matching_assignment_rules_with_tasks(tasks) -> list:
    result = {}

    try:
        matching_task_count = 0

        for task in tasks:
            # check if task is already matched with another rules
            # get all assignment rules
            assignment_rules = AssigmentRule.objects.filter(
                work_center=task.work_center, is_active=True
            ).order_by("order")

            if assignment_rules:
                for rule in assignment_rules:
                    # get all rule criteria for the rule
                    rule_criteria = AssigmentRuleCriteria.objects.filter(
                        assigment_rule=rule
                    )

                    criteria_match = False
                    if rule_criteria:
                        # check if any rule criteria matches the task
                        for criteria in rule_criteria:
                            if check_criteria_match(task, criteria):
                                criteria_match = True
                                matching_task_count += 1

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
                            # if criteria match store it in the TaskRuleAssignment model
                            task_rule_instance = TaskRuleAssignment.objects.create(
                                task=task,
                                assigment_rule=rule,
                                is_applied=is_rule_applied,
                            )
                            task_rule_instance.save()

                    else:
                        # if not criteria match, delete the TaskRuleAssignment model instance if exists
                        task_rule_assignment = TaskRuleAssignment.objects.filter(
                            task=task, assigment_rule=rule
                        )
                        if task_rule_assignment.exists():
                            task_rule_assignment.delete()

        result["message"] = f"Matched {matching_task_count} tasks with assignment rules"
        result["status"] = "success"

        return result
    except Exception as e:
        result["message"] = str(e)
        result["status"] = "error"
        return result
