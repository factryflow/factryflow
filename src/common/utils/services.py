from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.reverse_related import ManyToOneRel
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
    # Checks if a criteria matches a task
    # Used in models where criteria is used to match with tasks
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
