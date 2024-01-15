from common.services import model_update
from django.contrib.auth.models import User
from resource_calendar.models import WeeklyShiftTemplate

from resource_manager.models import Resource, ResourcePool, WorkUnit


class ResourceService:
    def __init__(self):
        pass

    def create(
        self,
        *,
        name: str,
        external_id: str = "",
        notes: str = "",
        work_units: list[WorkUnit] = None,
        resource_pools: list[ResourcePool] = None,
        users: list[User] = None,
        weekly_shift_template: WeeklyShiftTemplate = None,
    ) -> Resource:
        resource = Resource.objects.create(
            name=name,
            external_id=external_id,
            weekly_shift_template=weekly_shift_template,
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
        fields = [
            "name",
            "external_id",
            "notes",
            "work_units",
            "resource_pools",
            "users",
            "weekly_shift_template",
        ]

        resource, _ = model_update(instance=instance, fields=fields, data=data)

        return resource

    def delete(self, instance: Resource) -> None:
        instance.delete()


class WorkUnitService:
    def __init__(self):
        pass

    def create(
        self,
        *,
        name: str,
        external_id: str = "",
        notes: str = "",
        resources: list[Resource] = None,
        resource_pools: list[ResourcePool] = None,
    ) -> WorkUnit:
        work_unit = WorkUnit.objects.create(
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
        fields = [
            "name",
            "external_id",
            "resources",
            "work_units",
            "notes",
        ]

        resource_pool, _ = model_update(instance=instance, fields=fields, data=data)

        return resource_pool

    def delete(self, instance: ResourcePool) -> None:
        instance.delete()
