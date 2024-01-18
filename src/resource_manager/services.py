from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from resource_calendar.models import WeeklyShiftTemplate

from resource_manager.models import Resource, ResourcePool, WorkUnit


<<<<<<< HEAD
class ResourceService:
    def __init__(self):
        pass

=======
class ResourceService(AbstractPermissionService):
>>>>>>> 59ba0bc (added permission check to all services)
    def create(
        self,
        *,
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
        if not self.check_for_permission("add_resource"):
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
        resource.save()

        return resource

    def update(self, *, instance: Resource, data: dict) -> Resource:
        # check permissions for update resource
        if not self.check_for_permission("change_resource"):
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

<<<<<<< HEAD
        resource, _ = model_update(instance=instance, fields=fields, data=data)
=======
        resource, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )
>>>>>>> 59ba0bc (added permission check to all services)

        return resource

    def delete(self, instance: Resource) -> None:
        # check permissions for delete resource
        if not self.check_for_permission("delete_resource"):
            raise PermissionDenied()

        instance.delete()


<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> c9eb050 (resolved conflicts)
class WorkUnitService:
    def __init__(self):
        pass

<<<<<<< HEAD
=======
class ResourceGroupService(AbstractPermissionService):
>>>>>>> 59ba0bc (added permission check to all services)
=======
>>>>>>> c9eb050 (resolved conflicts)
    def create(
        self,
        *,
        name: str,
        external_id: str = "",
        notes: str = "",
        resources: list[Resource] = None,
<<<<<<< HEAD
<<<<<<< HEAD
        resource_pools: list[ResourcePool] = None,
    ) -> WorkUnit:
        work_unit = WorkUnit.objects.create(
=======
    ) -> ResourceGroup:
        # check permissions for add resource group
        if not self.check_for_permission("add_resourcegroup"):
            raise PermissionDenied()

        resource_group = ResourceGroup.objects.create(
>>>>>>> 59ba0bc (added permission check to all services)
=======
        resource_pools: list[ResourcePool] = None,
    ) -> WorkUnit:
        work_unit = WorkUnit.objects.create(
>>>>>>> c9eb050 (resolved conflicts)
            name=name,
            external_id=external_id,
            notes=notes,
        )

        work_unit.full_clean()
        work_unit.save()

        if resources:
            work_unit.resources.set(resources)

        if resource_pools:
            work_unit.resource_pools.set(resource_pools)

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> c9eb050 (resolved conflicts)
        return work_unit

    def update(self, *, instance: WorkUnit, data: dict) -> WorkUnit:
        fields = [
            "name",
            "external_id",
            "notes",
            "resources",
            "resource_pools",
        ]

        work_unit, _ = model_update(instance=instance, fields=fields, data=data)

        return work_unit

    def delete(self, instance: WorkUnit) -> None:
        instance.delete()


class ResourcePoolService:
    def __init__(self):
        pass

    def create(
        self,
        *,
        name: str,
        external_id: str = "",
        notes: str = "",
        resources: list[Resource] = None,
        work_units: list[WorkUnit] = None,
    ) -> ResourcePool:
        resource_pool = ResourcePool.objects.create(
            name=name,
            external_id=external_id,
            notes=notes,
        )

        resource_pool.full_clean()
        resource_pool.save()

        if resources:
            resource_pool.resources.set(resources)

        if work_units:
            resource_pool.work_units.set(work_units)

        return resource_pool

    def update(self, *, instance: ResourcePool, data: dict) -> ResourcePool:
<<<<<<< HEAD
=======
    def update(self, *, instance: ResourceGroup, data: dict) -> ResourceGroup:
        # check permissions for update resource group
        if not self.check_for_permission("change_resourcegroup"):
            raise PermissionDenied()

>>>>>>> 59ba0bc (added permission check to all services)
=======
>>>>>>> c9eb050 (resolved conflicts)
        fields = [
            "name",
            "external_id",
            "resources",
            "work_units",
            "notes",
        ]

<<<<<<< HEAD
<<<<<<< HEAD
        resource_pool, _ = model_update(instance=instance, fields=fields, data=data)
=======
        resource_group, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )
>>>>>>> 59ba0bc (added permission check to all services)

        return resource_pool

<<<<<<< HEAD
    def delete(self, instance: ResourcePool) -> None:
=======
    def delete(self, instance: ResourceGroup) -> None:
        # check permissions for delete resource group
        if not self.check_for_permission("delete_resourcegroup"):
            raise PermissionDenied()

>>>>>>> 59ba0bc (added permission check to all services)
=======
        resource_pool, _ = model_update(instance=instance, fields=fields, data=data)

        return resource_pool

    def delete(self, instance: ResourcePool) -> None:
>>>>>>> c9eb050 (resolved conflicts)
        instance.delete()
