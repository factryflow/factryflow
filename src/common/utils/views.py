import json

from django.http import HttpResponse
from django.apps import apps
from django.db.models.fields.reverse_related import ManyToOneRel

from .constants import get_html_input_type, NOT_REQUIRED_FIELDS_IN_FORM


def add_notification_headers(
    response: HttpResponse, notification_content: str, notification_type: str = "info"
) -> HttpResponse:
    # Adds a custom 'hx-trigger' header to the HttpResponse for triggering a notification.
    allowed_types = ["info", "success", "error"]

    # Validate notification type
    if notification_type not in allowed_types:
        raise ValueError(
            f"Invalid notification type: {notification_type}. Allowed types are {allowed_types}"
        )

    notification_data = json.dumps(
        {
            "notify": {
                "content": notification_content,
                "type": notification_type,
            }
        }
    )

    response["hx-trigger"] = notification_data
    return response


def convert_datetime_to_readable_string(datetime: str) -> str:
    # Converts a datetime string to a human-readable string.
    return datetime.strftime("%B %d, %Y %I:%M %p")


def convert_date_to_readable_string(date: str) -> str:
    # Converts a date string to a human-readable string.
    return date.strftime("%B %d, %Y")


def convert_timestamp(datetime: str) -> str:
    # Converts a datetime object to "DD-MM-YYYY HH:MM"
    return datetime.strftime("%d-%m-%Y %H:%M")


def convert_date(datetime: str) -> str:
    # Converts a datetime object to "DD-MM-YYYY"
    return datetime.strftime("%d-%m-%Y")


def get_related_fields(model, related_field_name, with_type=False):
    """
    Get the names of the fields in the related model of a given model's related field.

    Args:
        model (django.db.models.Model): The model class.
        related_field_name (str): The name of the related field.

    Returns:
        list: A list of field names in the related model.

    """
    related_model = model._meta.get_field(related_field_name).related_model

    if with_type:
        fields = [
            (field.name, get_html_input_type(field.get_internal_type()))
            for field in related_model._meta.get_fields()
            if not isinstance(field, ManyToOneRel)
            and field.name not in NOT_REQUIRED_FIELDS_IN_FORM
        ]
    else:
        fields = [
            field.name
            for field in related_model._meta.get_fields()
            if not isinstance(field, ManyToOneRel)
            and field.name not in NOT_REQUIRED_FIELDS_IN_FORM
        ]

    return fields


def get_model_fields(model_name, app_name, related_field_names, with_type=False):
    """
    Get the fields of a model.

    Args:
        model_name (str): The name of the model.
        app_name (str): The name of the app containing the model.
        related_field_names (list): A list of related field names.

    Returns:
        list: A list of tuples containing the field names and their display names with type.
    """

    # get the model using the app name and model name
    model = apps.get_model(app_name, model_name)

    if with_type:
        # the fields of the model
        fields = [
            (field.name, get_html_input_type(field.get_internal_type()))
            for field in model._meta.get_fields()
            if not isinstance(field, ManyToOneRel)
            and field.name not in NOT_REQUIRED_FIELDS_IN_FORM
        ]
    else:
        # the fields of the model
        fields = [
            (field.name, field.name)
            for field in model._meta.get_fields()
            if not isinstance(field, ManyToOneRel)
            and field.name not in NOT_REQUIRED_FIELDS_IN_FORM
        ]

    # get the related fields for each related field name
    for related_field_name in related_field_names:
        if with_type:
            related_fields_with_type = get_related_fields(
                model, related_field_name, with_type=True
            )
            fields.extend(
                [
                    (
                        f"{related_field_name}.{field_name}",
                        field_type,
                    )
                    for field_name, field_type in related_fields_with_type
                ]
            )
        else:
            related_fields = get_related_fields(model, related_field_name)
            fields.extend(
                [
                    (
                        f"{related_field_name}.{field_name}",
                        f"{related_field_name}-{field_name}",
                    )
                    for field_name in related_fields
                ]
            )

    return fields
