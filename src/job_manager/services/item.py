from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied
from django.db import transaction

from job_manager.models import Item


# ------------------------------------------------------------------------------
# Item Services
# ------------------------------------------------------------------------------


class ItemService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self,
        name: str,
        description: str = "",
        external_id: str = "",
        notes: str = "",
        custom_fields: dict = None,
    ) -> Item:
        # check for permission to create item
        if not self.permission_service.check_for_permission("add_item"):
            raise PermissionDenied()

        item = Item.objects.create(
            name=name,
            description=description,
            external_id=external_id,
            notes=notes,
            custom_fields=custom_fields,
        )
        item.full_clean()
        item.save(user=self.user)

        return item

    @transaction.atomic
    def update(self, instance: Item, data: dict) -> Item:
        # check for permission to update item
        if not self.permission_service.check_for_permission("change_item"):
            raise PermissionDenied()

        fields = [
            "name",
            "description",
            "external_id",
            "notes",
            "custom_fields",
        ]

        item, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return item

    @transaction.atomic
    def delete(self, instance: Item) -> None:
        # check for permission to delete item
        if not self.permission_service.check_for_permission("delete_item"):
            raise PermissionDenied()

        instance.delete()
        return True
