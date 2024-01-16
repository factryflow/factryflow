from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from resource_calendar.models import WeeklyShiftTemplate

from resource_manager.models import Resource, ResourceGroup


class ResourceService(AbstractPermissionService):
    def create(
        self,
        *,
        name: str,
        external_id: str = "",
        notes: str = "",
        resource_groups: list[ResourceGroup] = None,
        users: list[User] = None,
        weekly_shift_template: WeeklyShiftTemplate = None,
    ) -> Resource:
        # check permissions for add resource
        if not self.check_for_permission("add_resource"):
            raise PermissionDenied()

        resource = Resource.objects.create(
            name=name,
            external_id=external_id,
            weekly_shift_template=weekly_shift_template,
            notes=notes,
        )

        if resource_groups:
            resource.resource_groups.set(resource_groups)

        if users:
            resource.users.set(users)

        resource.full_clean()
        resource.save(user=self.user)

        return resource

    def update(self, *, instance: Resource, data: dict) -> Resource:
        # check permissions for update resource
        if not self.check_for_permission("change_resource"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "notes",
            "resource_groups",
            "users",
            "weekly_shift_template",
        ]

        resource, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return resource

    def delete(self, instance: Resource) -> None:
        # check permissions for delete resource
        if not self.check_for_permission("delete_resource"):
            raise PermissionDenied()

        instance.delete()


class ResourceGroupService(AbstractPermissionService):
    def create(
        self,
        *,
        name: str,
        external_id: str = "",
        notes: str = "",
        resources: list[Resource] = None,
    ) -> ResourceGroup:
        # check permissions for add resource group
        if not self.check_for_permission("add_resourcegroup"):
            raise PermissionDenied()

        resource_group = ResourceGroup.objects.create(
            name=name,
            external_id=external_id,
            notes=notes,
        )

        resource_group.full_clean()
        resource_group.save(user=self.user)

        if resources:
            resource_group.resources.set(resources)

        return resource_group

    def update(self, *, instance: ResourceGroup, data: dict) -> ResourceGroup:
        # check permissions for update resource group
        if not self.check_for_permission("change_resourcegroup"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "resources",
            "notes",
        ]

        resource_group, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return resource_group

    def delete(self, instance: ResourceGroup) -> None:
        # check permissions for delete resource group
        if not self.check_for_permission("delete_resourcegroup"):
            raise PermissionDenied()

        instance.delete()
