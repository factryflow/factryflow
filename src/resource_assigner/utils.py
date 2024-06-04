from django.apps import apps
from django.db.models.fields.reverse_related import ManyToOneRel

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
