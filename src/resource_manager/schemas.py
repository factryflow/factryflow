from ninja import Field, ModelSchema

from resource_manager.models import Resource, ResourcePool


class ResourcePoolIn(ModelSchema):
    resources: list[int] = Field(None, alias="resource_ids")
    work_units: list[int] = Field(None, alias="work_unit_ids")

    class Meta:
        model = ResourcePool
        fields = ["name", "external_id", "notes"]


class ResourcePoolOut(ModelSchema):
    resource_ids: list[int] = Field([], alias="resource_id_list")
    work_unit_ids: list[int] = Field([], alias="work_unit_id_list")

    class Meta:
        model = ResourcePool
        exclude = ["work_units"]


class ResourceIn(ModelSchema):
    # resource_pools: list[int] = Field(None, alias="resource_pool_ids")
    users: list[int] = Field(None, alias="user_ids")
    work_units: list[int] = Field(None, alias="work_unit_ids")

    class Meta:
        model = Resource
        fields = ["name", "external_id", "notes"]


class ResourceOut(ModelSchema):
    # resource_pool_ids: list[int] = Field([], alias="resource_pool_id_list")
    user_ids: list[int] = Field([], alias="user_id_list")
    work_unit_ids: list[int] = Field([], alias="work_unit_id_list")

    class Meta:
        model = Resource
        exclude = ["users", "work_units"]


class WorkUnitIn(ModelSchema):
    resource_pools: list[int] = Field(None, alias="resource_pool_ids")

    class Meta:
        model = Resource
        fields = ["name", "external_id", "notes"]


class WorkUnitOut(ModelSchema):
    resource_pool_ids: list[int] = Field([], alias="resource_pool_id_list")

    class Meta:
        model = Resource
        fields = "__all__"
