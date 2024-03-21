from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from resource_calendar.models import WeeklyShiftTemplate

from resource_manager.models import Resource, ResourcePool, WorkUnit


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
        work_units: list[WorkUnit] = None,
        resource_pools: list[ResourcePool] = None,
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

        if work_units:
            resource.work_units.set(work_units)

        if resource_pools:
            resource.resource_pools.set(resource_pools)

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
            "work_units",
            "resource_pools",
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


class WorkUnitService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self,
        name: str,
        external_id: str = "",
        notes: str = "",
    ) -> WorkUnit:
        # check permissions for add workunit
        if not self.permission_service.check_for_permission("add_workunit"):
            raise PermissionDenied()

        work_unit = WorkUnit.objects.create(
            name=name,
            external_id=external_id,
            notes=notes,
        )

        work_unit.full_clean()
        work_unit.save(user=self.user)

        return work_unit

    def update(self, instance: WorkUnit, data: dict) -> WorkUnit:
        # check permissions for update work unit
        if not self.permission_service.check_for_permission("change_workunit"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "notes",
        ]

        work_unit, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return work_unit

    def delete(self, instance: WorkUnit) -> None:
        # check permission for delete work unit
        if not self.permission_service.check_for_permission("delete_workunit"):
            raise PermissionDenied()

        instance.delete()


class ResourcePoolService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self,
        name: str,
        external_id: str = "",
        notes: str = "",
        parent: ResourcePool = None,
        resources: list[Resource] = None,
        work_units: list[WorkUnit] = None,
    ) -> ResourcePool:
        # check permissions for add resource pool
        if not self.permission_service.check_for_permission("add_resourcepool"):
            raise PermissionDenied()

        resource_pool = ResourcePool.objects.create(
            name=name,
            external_id=external_id,
            notes=notes,
            parent=parent,
        )

        resource_pool.full_clean()
        resource_pool.save(user=self.user)

        if work_units:
            resource_pool.work_units.set(work_units)
        
        if resources:
            resource_pool.resources.set(resources)

        return resource_pool

    def update(self, instance: ResourcePool, data: dict) -> ResourcePool:
        # check permissions for update resource pool
        if not self.permission_service.check_for_permission("change_resourcepool"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "parent",
            "work_units",
            "resources",
            "notes",
        ]

        resource_pool, _ = model_update(instance=instance, fields=fields, data=data)

        return resource_pool

    def delete(self, instance: ResourcePool) -> None:
        # check permissions for delete resource pool
        if not self.permission_service.check_for_permission("delete_resourcepool"):
            raise PermissionDenied()

        instance.delete()
