from typing import Any, Dict, List, Tuple

from api.permission_checker import AbstractPermissionService
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models.fields.related import ManyToManyRel
from django.utils import timezone

from common.models import CustomField
from common.types import DjangoModelType


def model_update(
    *,
    user=None,
    instance: DjangoModelType,
    fields: List[str],
    data: Dict[str, Any],
    auto_updated_at=True,
) -> Tuple[DjangoModelType, bool]:
    """
    Generic update service meant to be reused in local update services.

    For example:

    def user_update(*, user: User, data) -> User:
        fields = ['first_name', 'last_name']
        user, has_updated = model_update(instance=user, fields=fields, data=data)

        // Do other actions with the user here

        return user

    Return value: Tuple with the following elements:
        1. The instance we updated.
        2. A boolean value representing whether we performed an update or not.

    Some important notes:

        - Only keys present in `fields` will be taken from `data`.
        - If something is present in `fields` but not present in `data`, we simply skip.
        - There's a strict assertion that all values in `fields` are actual fields in `instance`.
        - `fields` can support m2m fields, which are handled after the update on `instance`.
        - If `auto_updated_at` is True, we'll try bumping `updated_at` with the current timestmap.
    """
    has_updated = False
    m2m_data = {}
    update_fields = []

    model_fields = {field.name: field for field in instance._meta.get_fields()}

    for field in fields:
        # Skip if a field is not present in the actual data
        if field not in data:
            continue

        # If field is not an actual model field, raise an error
        model_field = model_fields.get(field)

        assert (
            model_field is not None
        ), f"{field} is not part of {instance.__class__.__name__} fields."

        # If we have m2m field, handle differently
        # include ManyToManyRel for reverse relations
        if isinstance(model_field, models.ManyToManyField) or isinstance(
            model_field, ManyToManyRel
        ):
            m2m_data[field] = data[field]
            continue

        if getattr(instance, field) != data[field]:
            has_updated = True
            update_fields.append(field)
            setattr(instance, field, data[field])

    # Perform an update only if any of the fields were actually changed
    if has_updated:
        if auto_updated_at:
            # We want to take care of the `updated_at` field,
            # Only if the models has that field
            # And if no value for updated_at has been provided
            if "updated_at" in model_fields and "updated_at" not in update_fields:
                update_fields.append("updated_at")
                instance.updated_at = timezone.now()  # type: ignore

        instance.full_clean()
        # Update only the fields that are meant to be updated.
        # Django docs reference:
        # https://docs.djangoproject.com/en/dev/ref/models/instances/#specifying-which-fields-to-save
        instance.save(update_fields=update_fields, user=user)

    for field_name, value in m2m_data.items():
        related_manager = getattr(instance, field_name)
        related_manager.set(value)

        # Still not sure about this.
        # What if we only update m2m relations & nothing on the model? Is this still considered as updated?
        has_updated = True

    return instance, has_updated


# ------------------------------------------------------------------------------
# CustomField Service
# ------------------------------------------------------------------------------


class CustomFieldService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def _add_prefix_to_name(self, name: str) -> str:
        return f"custom_{name}"

    def create(
        self,
        name: str,
        label: str,
        field_type: str,
        is_required: bool,
        content_type: ContentType,
        custom_fields: dict = None,
        description: str = "",
    ):
        # check permissions for add custom field
        if not self.permission_service.check_for_permission("add_customfield"):
            raise PermissionDenied()

        if not name.startswith("custom_"):
            name = self._add_prefix_to_name(name)

        custom_field = CustomField.objects.create(
            content_type=content_type,
            name=name,
            label=label,
            description=description,
            field_type=field_type,
            custom_fields=custom_fields,
            is_required=is_required,
        )
        custom_field.full_clean()
        custom_field.save(user=self.user)

        return custom_field

    def update(self, instance: CustomField, data: dict):
        # check permissions for update custom field
        if not self.permission_service.check_for_permission("change_customfield"):
            raise PermissionDenied()

        # add prefix to name
        if "name" in data and not data["name"].startswith("custom_"):
            data["name"] = self._add_prefix_to_name(data["name"])

        fields = [
            "name",
            "label",
            "description",
            "is_required",
            "custom_fields",
            "field_type",
            "content_type",
        ]
        custom_field, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )
        return custom_field

    def delete(self, instance: CustomField):
        # check permissions for delete custom field
        if not self.permission_service.check_for_permission("delete_customfield"):
            raise PermissionDenied()

        instance.delete()

        return True
