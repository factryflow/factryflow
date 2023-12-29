from ninja import Field, ModelSchema

from job_manager.models import (
    Job,
    JobType,
)


class JobTypeIn(ModelSchema):
    class Meta:
        model = JobType
        fields = ["name"]


class JobTypeOut(ModelSchema):
    class Meta:
        model = JobType
        fields = "__all__"


class JobIn(ModelSchema):
    dependencies: list[int] = Field(None, alias="dependency_ids")

    class Meta:
        model = Job
        fields = [
            "name",
            "external_id",
            "job_type",
            "job_status",
            "note",
            "description",
            "due_date",
            "customer",
            "priority",
            "planned_start_datetime",
            "planned_end_datetime",
        ]


class JobOut(ModelSchema):
    class Meta:
        model = Job
        fields = "__all__"
