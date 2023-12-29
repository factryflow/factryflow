from ninja import Field, ModelSchema

from job_manager.models import (
    Dependency,
    DependencyType,
    DependencyStatusChoices,
)


class DependencyTypeIn(ModelSchema):
    class Meta:
        model = DependencyType
        fields = ["name"]


class DependencyTypeOut(ModelSchema):
    class Meta:
        model = DependencyType
        fields = "__all__"


class DependencyIn(ModelSchema):
    dependency_status: DependencyStatusChoices = Field(None, alias="dependencyStatus")

    class Meta:
        model = Dependency
        fields = [
            "name",
            "external_id",
            "dependency_type",
            "expected_close_datetime",
            "notes",
            "actual_close_datetime",
        ]


class DependencyOut(ModelSchema):
    class Meta:
        model = Dependency
        fields = "__all__"

