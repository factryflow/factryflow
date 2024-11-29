from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied

from resource_manager.models import Resource, ResourceGroup


# ------------------------------------------------------------------------------
# ResourceGroup Service
# ------------------------------------------------------------------------------


class ResourceGroupService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self,
        name: str,
        external_id: str = "",
        notes: str = "",
        parent: ResourceGroup = None,
        resources: list[Resource] = None,
        custom_fields: dict = None,
    ) -> ResourceGroup:
        # check permissions for add resource pool
        if not self.permission_service.check_for_permission("add_resourcegroup"):
            raise PermissionDenied()

        resource_group = ResourceGroup.objects.create(
            name=name,
            external_id=external_id,
            notes=notes,
            parent=parent,
            custom_fields=custom_fields,
        )

        resource_group.full_clean()
        resource_group.save(user=self.user)

        if resources:
            resource_group.resources.set(resources)

        return resource_group

    def update(self, instance: ResourceGroup, data: dict) -> ResourceGroup:
        # check permissions for update resource pool
        if not self.permission_service.check_for_permission("change_resourcegroup"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "parent",
            "resources",
            "notes",
            "custom_fields",
        ]

        resource_group, _ = model_update(instance=instance, fields=fields, data=data)

        return resource_group

    def delete(self, instance: ResourceGroup) -> None:
        # check permissions for delete resource pool
        if not self.permission_service.check_for_permission("delete_resourcegroup"):
            raise PermissionDenied()

        instance.delete()
        return True
