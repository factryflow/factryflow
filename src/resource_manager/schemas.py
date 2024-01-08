from ninja import Field, ModelSchema

from resource_manager.models import Resource, ResourceGroup


class ResourceGroupIn(ModelSchema):
    resources: list[int] = Field(None, alias="resource_ids")

    class Meta:
        model = ResourceGroup
        fields = ["name", "external_id"]


class ResourceGroupOut(ModelSchema):
    resource_ids: list[int] = Field([], alias="resource_id_list")

    class Meta:
        model = ResourceGroup
        fields = "__all__"


class ResourceIn(ModelSchema):
    resource_groups: list[int] = Field(None, alias="resource_group_ids")
    users: list[int] = Field(None, alias="user_ids")

    class Meta:
        model = Resource
        fields = ["name", "external_id"]


class ResourceOut(ModelSchema):
    resource_group_ids: list[int] = Field([], alias="resource_group_id_list")
    user_ids: list[int] = Field([], alias="user_id_list")

    class Meta:
        model = Resource
        exclude = ["resource_groups", "users"]
