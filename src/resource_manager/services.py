from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from resource_calendar.models import WeeklyShiftTemplate

from resource_manager.models import Resource, ResourceGroup


# ------------------------------------------------------------------------------
# Resource Service
# ------------------------------------------------------------------------------


class ResourceService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self,
        name: str,
        external_id: str = "",
        notes: str = "",
        resource_type: str = None,
        users: list[User] = None,
        weekly_shift_template: WeeklyShiftTemplate = None,
    ) -> Resource:
        # check permissions for add resource
        if not self.permission_service.check_for_permission("add_resource"):
            raise PermissionDenied()

        resource = Resource.objects.create(
            name=name,
            external_id=external_id,
            weekly_shift_template=weekly_shift_template,
            resource_type=resource_type,
            notes=notes,
        )

        if users:
            resource.users.set(users)

        resource.full_clean()
        resource.save(user=self.user)

        return resource

    def update(self, instance: Resource, data: dict) -> Resource:
        # check permissions for update resource
        if not self.permission_service.check_for_permission("change_resource"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "notes",
            "users",
            "weekly_shift_template",
        ]

        resource, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return resource

    def delete(self, instance: Resource) -> None:
        # check permissions for delete resource
        if not self.permission_service.check_for_permission("delete_resource"):
            raise PermissionDenied()

        instance.delete()
        return True


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
    ) -> ResourceGroup:
        # check permissions for add resource pool
        if not self.permission_service.check_for_permission("add_resourcegroup"):
            raise PermissionDenied()

        resource_group = ResourceGroup.objects.create(
            name=name,
            external_id=external_id,
            notes=notes,
            parent=parent,
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
        ]

        resource_group, _ = model_update(instance=instance, fields=fields, data=data)

        return resource_group

    def delete(self, instance: ResourceGroup) -> None:
        # check permissions for delete resource pool
        if not self.permission_service.check_for_permission("delete_resourcegroup"):
            raise PermissionDenied()

        instance.delete()
        return True
