from django.apps import apps
from django.db.models.fields.reverse_related import ManyToOneRel


from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    Operator,
    TaskResourceAssigment,
)

from job_manager.models import TaskStatusChoices, JobStatusChoices


# Fields that are not required in the form
NOT_REQUIRED_FIELDS_IN_FORM = [
    "created_at",
    "updated_at",
    "created_by",
    "updated_by",
    "custom_fields",
]


def get_related_fields(model, related_field_name):
    """
    Get the names of the fields in the related model of a given model's related field.

    Args:
        model (django.db.models.Model): The model class.
        related_field_name (str): The name of the related field.

    Returns:
        list: A list of field names in the related model.

    """
    related_model = model._meta.get_field(related_field_name).related_model

    fields = [
        field.name
        for field in related_model._meta.get_fields()
        if not isinstance(field, ManyToOneRel)
        and field.name not in NOT_REQUIRED_FIELDS_IN_FORM
    ]

    return fields


def get_model_fields(model_name, app_name, related_field_names):
    """
    Get the fields of a model.

    Args:
        model_name (str): The name of the model.
        app_name (str): The name of the app containing the model.
        related_field_names (list): A list of related field names.

    Returns:
        list: A list of tuples containing the field names and their display names.
    """

    # get the model using the app name and model name
    model = apps.get_model(app_name, model_name)

    # the fields of the model
    fields = [
        (field.name, field.name)
        for field in model._meta.get_fields()
        if not isinstance(field, ManyToOneRel)
        and field.name not in NOT_REQUIRED_FIELDS_IN_FORM
    ]

    # get the related fields for each related field name
    for related_field_name in related_field_names:
        related_fields = get_related_fields(model, related_field_name)
        fields.extend(
            [
                (
                    f"{related_field_name}.{field_name}",
                    f"{related_field_name}.{field_name}",
                )
                for field_name in related_fields
            ]
        )

    return fields


def check_criteria_match(task, criteria):
    # check if the criteria matches the task
    field = criteria.field
    operator = criteria.operator
    value = criteria.value

    # get task value for the field
    task_value = str(getattr(task, field))

    # check if the task value matches the criteria value
    if operator == Operator.EQUALS:
        return task_value == value
    elif operator == Operator.CONTAINS:
        return value in task_value
    elif operator == Operator.STARTS_WITH:
        return task_value.startswith(value)
    elif operator == Operator.ENDS_WITH:
        return task_value.endswith(value)
    elif operator == Operator.GREATER_THAN:
        return task_value > value
    elif operator == Operator.LESS_THAN:
        return task_value < value

    return False


def get_matching_assignment_rules_with_tasks(tasks) -> list:
    result = {}

    try:
        matching_task_count = 0

        for task in tasks:
            # check if task is already matched with another rules
            if not TaskResourceAssigment.objects.filter(task=task).exists():
                # get all assignment rules
                assignment_rules = AssigmentRule.objects.filter(
                    work_center=task.work_center
                )

                if assignment_rules:
                    for rule in assignment_rules:
                        # get all rule criteria for the rule
                        rule_criteria = AssigmentRuleCriteria.objects.filter(
                            assigment_rule=rule
                        )

                        if rule_criteria:
                            # check if any rule criteria matches the task
                            for criteria in rule_criteria:
                                if check_criteria_match(task, criteria):
                                    # if criteria match store it in the TaskResourceAssigment model
                                    TaskResourceAssigment.objects.create(
                                        task=task,
                                        assigment_rule=rule,
                                    )

                                    # update the task status to IN_PROGRESS
                                    task.task_status = TaskStatusChoices.IN_PROGRESS
                                    task.save()

                                    # update the job status to IN_PROGRESS
                                    task.job.job_status = JobStatusChoices.IN_PROGRESS
                                    task.job.save()

                                    matching_task_count += 1
                                    break

            result["message"] = (
                f"Matched {matching_task_count} tasks with assignment rules"
            )
            result["status"] = "success"

            return result
    except Exception as e:
        result["message"] = str(e)
        result["status"] = "error"
        return result
