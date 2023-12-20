from ninja import Field, ModelSchema

from resource_manager.models import Resource


class ResourceIn(ModelSchema):
    resource_groups: list[int] = Field(None, alias="resource_group_ids")

    class Meta:
        model = Resource
        fields = ["name", "external_id"]


class ResourceOut(ModelSchema):
    class Meta:
        model = Resource
        fields = "__all__"
