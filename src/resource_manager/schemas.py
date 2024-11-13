from ninja import Field, ModelSchema

from resource_manager.models import Resource, ResourceGroup


class ResourceGroupIn(ModelSchema):
    resources: list[int] = Field(None, alias="resource_ids")

    class Meta:
        model = ResourceGroup
        fields = ["name", "external_id", "notes", "parent", "custom_fields"]


class ResourceGroupOut(ModelSchema):
    class Meta:
        model = ResourceGroup
        fields = "__all__"


class ResourceIn(ModelSchema):
    class Meta:
        model = Resource
        fields = [
            "name",
            "users",
            "external_id",
            "notes",
            "resource_type",
            "weekly_shift_template",
            "custom_fields",
        ]


class ResourceOut(ModelSchema):
    class Meta:
        model = Resource
        fields = "__all__"
