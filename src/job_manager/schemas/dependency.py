from ninja import Field, ModelSchema

from job_manager.models import (
    Dependency,
    DependencyType,
)

# ------------------------------------------------------------------------------
# DependencyType Schemas
# ------------------------------------------------------------------------------


class DependencyTypeIn(ModelSchema):
    class Meta:
        model = DependencyType
        fields = ["name", "external_id", "notes", "custom_fields"]


class DependencyTypeOut(ModelSchema):
    class Meta:
        model = DependencyType
        fields = "__all__"


# ------------------------------------------------------------------------------
# Dependency Schemas
# ------------------------------------------------------------------------------


class DependencyIn(ModelSchema):
    class Meta:
        model = Dependency
        fields = [
            "name",
            "external_id",
            "dependency_type",
            "dependency_status",
            "expected_close_datetime",
            "notes",
            "custom_fields",
        ]


class DependencyOut(ModelSchema):
    class Meta:
        model = Dependency
        fields = "__all__"
