from ninja import Field, ModelSchema

from resource_manager.models import Resource


# ------------------------------------------------------------------------------
# Resource Schemas
# ------------------------------------------------------------------------------


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
