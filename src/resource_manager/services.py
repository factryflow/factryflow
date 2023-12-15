from common.services import model_update

from resource_manager.models import Resource, ResourceGroup


class ResourceService:
    def __init__(self):
        pass

    def create(
        name: str,
        resource_groups: list[ResourceGroup] = None,
        external_id: str = "",
    ) -> Resource:
        resource = Resource.objects.create(
            name=name,
            external_id=external_id,
        )

        if resource_groups:
            resource.resource_groups.set(resource_groups)

        resource.full_clean()
        resource.save()

        return resource

    def update(resource: Resource, data: dict) -> Resource:
        fields = [
            "name",
            "external_id",
        ]

        resource, _ = model_update(instance=resource, fields=fields, data=data)

        return resource

    def delete(resource: Resource) -> None:
        resource.delete()


class ResourceGroupService:
    def __init__(self):
        pass

    def create(
        name: str,
        external_id: str = "",
    ) -> ResourceGroup:
        resource_group = ResourceGroup.objects.create(
            name=name,
            external_id=external_id,
        )

        resource_group.full_clean()
        resource_group.save()

        return resource_group

    def update(resource_group: ResourceGroup, data: dict) -> ResourceGroup:
        fields = [
            "name",
            "external_id",
        ]

        resource_group, _ = model_update(
            instance=resource_group, fields=fields, data=data
        )

        return resource_group

    def delete(resource_group: ResourceGroup) -> None:
        resource_group.delete()
