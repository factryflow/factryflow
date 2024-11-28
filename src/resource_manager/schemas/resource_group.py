from ninja import Field, ModelSchema

from resource_manager.models import Resource, ResourceGroup


# ------------------------------------------------------------------------------
# ResourceGroup Schemas
# ------------------------------------------------------------------------------


class ResourceGroupIn(ModelSchema):
    resources: list[int] = Field(None, alias="resource_ids")

    class Meta:
        model = ResourceGroup
        fields = ["name", "external_id", "notes", "parent", "custom_fields"]


class ResourceGroupOut(ModelSchema):
    class Meta:
        model = ResourceGroup
        fields = "__all__"
