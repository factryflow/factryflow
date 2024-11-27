from api.permission_checker import AbstractPermissionService
from common.services import model_update
from users.models import User
from django.core.exceptions import PermissionDenied
from resource_calendar.models import WeeklyShiftTemplate

from resource_manager.models import Resource


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
        custom_fields: dict = None,
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
            custom_fields=custom_fields,
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
            "custom_fields",
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
