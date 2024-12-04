from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import get_object_or_404

from common.models import Operator


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def assert_settings(required_settings, error_message_prefix=""):
    """
    Validates if each item from `required_settings` is present in Django settings.
    """
    not_present = []
    values = {}

    for required_setting in required_settings:
        if not hasattr(settings, required_settings):
            not_present.append(required_setting)
            continue

        values[required_setting] = getattr(settings, required_setting)

    if not_present:
        if not error_message_prefix:
            error_message_prefix = "Required settings not found."

        stringified_not_present = ", ".join(not_present)

        raise ImproperlyConfigured(
            f"{error_message_prefix}: Could not find: {stringified_not_present}"
        )

    return values


def check_criteria_match(task, criteria):
    """
    Check if a task matches a given criteria.
    Args:
        task (object): The task object to be checked.
        criteria (object): The criteria object containing the field, operator, and value to check against.
    Returns:
        bool: True if the task matches the criteria, False otherwise.
    The criteria object should have the following attributes:
        - field (str): The field name to check in the task. It can be a nested field using dot notation (e.g., 'related_object.field').
        - operator (Operator): The operator to use for comparison. Supported operators are:
    """
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
