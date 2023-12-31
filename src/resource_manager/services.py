from common.services import model_update
from resource_calendar.models import WeeklyShiftTemplate

from resource_manager.models import Resource, ResourceGroup


class ResourceService:
    def __init__(self):
        pass

    def create(
        self,
        *,
        name: str,
        external_id: str = "",
        resource_groups: list[ResourceGroup] = None,
        weekly_shift_template: WeeklyShiftTemplate = None,
    ) -> Resource:
        resource = Resource.objects.create(
            name=name,
            external_id=external_id,
            weekly_shift_template=weekly_shift_template,
        )

        if resource_groups:
            resource.resource_groups.set(resource_groups)

        resource.full_clean()
        resource.save()

        return resource

    def update(self, *, instance: Resource, data: dict) -> Resource:
        fields = ["name", "external_id", "resource_groups", "weekly_shift_template"]

        resource, _ = model_update(instance=instance, fields=fields, data=data)

        return resource

    def delete(self, instance: Resource) -> None:
        instance.delete()


class ResourceGroupService:
    def __init__(self):
        pass

    def create(
        self,
        *,
        name: str,
        external_id: str = "",
        resources: list[Resource] = None,
    ) -> ResourceGroup:
        resource_group = ResourceGroup.objects.create(
            name=name,
            external_id=external_id,
        )

        resource_group.full_clean()
        resource_group.save()

        if resources:
            resource_group.resources.set(resources)

        return resource_group

    def update(self, *, instance: ResourceGroup, data: dict) -> ResourceGroup:
        fields = [
            "name",
            "external_id",
            "resources",
        ]

        resource_group, _ = model_update(instance=instance, fields=fields, data=data)

        return resource_group

    def delete(self, instance: ResourceGroup) -> None:
        instance.delete()
