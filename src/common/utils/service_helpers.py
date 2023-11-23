from django.core.exceptions import ValidationError


def create_or_update_model(model, data: dict):
    """
    Create or update a Django model instance based on the provided data.

    :param model: The Django model class.
    :param data: Dictionary containing data for the model instance.
    :return: The created or updated model instance.
    """
    model_id = data.get("id")
    if model_id:
        instance = model.objects.filter(id=model_id).first()
        if not instance:
            raise ValidationError(f"{model.__name__} with given id does not exist.")
        for key, value in data.items():
            setattr(instance, key, value)
    else:
        instance = model(**data)

    return instance
