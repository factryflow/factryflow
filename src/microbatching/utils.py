from common.utils.services import check_criteria_match

from microbatching.models.microbatch_rule import (
    MicrobatchRule,
    MicrobatchRuleCriteria,
    MicrobatchRuleTaskMatch,
)


def create_microbatch_rule_matches(tasks) -> list:
    result = {}

    try:
        matching_task_count = 0

        for task in tasks:
            # check if task is already matched with other rules
            # get all microbatch rules
            microbatch_rules = MicrobatchRule.objects.filter(
                work_center=task.work_center, is_active=True
            )

            if microbatch_rules:
                for rule in microbatch_rules:
                    # get all rule criteria for the rule
                    rule_criteria = MicrobatchRuleCriteria.objects.filter(
                        microbatch_rule=rule
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
