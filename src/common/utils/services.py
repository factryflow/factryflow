from typing import Type

from django.core.exceptions import ValidationError
from django.db.models import Model


def build_or_retrieve_instance(
    model: Type[Model], data: dict, allowed_fields: list = None
) -> (Model, str):
    """
    Create or update a Django model instance based on the provided data.
    """

    if allowed_fields is not None:
        data = {k: v for k, v in data.items() if k in allowed_fields}

    model_id = data.pop("id", None)
    action = "update" if model_id else "create"
    if action == "update":
        instance = model.objects.filter(id=model_id).first()
        if not instance:
            raise ValidationError(f"{model.__name__} with given id does not exist.")
        for key, value in data.items():
            setattr(instance, key, value)
    else:
        instance = model(**data)

    return (instance, action)
