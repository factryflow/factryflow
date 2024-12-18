from api.permission_checker import AbstractPermissionService
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

from common.models import CustomField
from .common import model_update


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
