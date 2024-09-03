from django.apps import apps
from django.db.models.fields.reverse_related import ManyToOneRel


from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    Operator,
    TaskRuleAssignment,
)


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

    # get the value of the field in the task
    if "." in field:
        # get the related object and field (foreign key field)
        related_object, field = field.split(".")
        task_value = (
            str(getattr(getattr(task, related_object), field))
            if hasattr(getattr(task, related_object), field)
            else None
        )
    else:
        # get the value of the field in the task
        task_value = str(getattr(task, field)) if hasattr(task, field) else None

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
                        is_rule_applied = True if rule.order == 0 else False

                        task_rule_instance = TaskRuleAssignment.objects.filter(
                            assigment_rule=rule, task=task
                        )

                        if task_rule_instance.exists():
                            task_rule_instance.first().is_applied = is_rule_applied
                            task_rule_instance.first().save()

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

            result["message"] = (
                f"Matched {matching_task_count} tasks with assignment rules"
            )
            result["status"] = "success"

            return result
    except Exception as e:
        result["message"] = str(e)
        result["status"] = "error"
        return result
