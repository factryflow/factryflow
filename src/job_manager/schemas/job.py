from ninja import Field, ModelSchema

from job_manager.models import (
    Job,
    JobType,
)

# ------------------------------------------------------------------------------
# JobType Schemas
# ------------------------------------------------------------------------------


class JobTypeIn(ModelSchema):
    class Meta:
        model = JobType
        fields = ["name", "external_id", "notes", "custom_fields"]


class JobTypeOut(ModelSchema):
    class Meta:
        model = JobType
        fields = "__all__"


# ------------------------------------------------------------------------------
# Job Schemas
# ------------------------------------------------------------------------------


class JobIn(ModelSchema):
    class Meta:
        model = Job
        fields = [
            "name",
            "external_id",
            "job_type",
            "job_status",
            "dependencies",
            "notes",
            "description",
            "due_date",
            "customer",
            "priority",
            "custom_fields",
        ]


class JobOut(ModelSchema):
    class Meta:
        model = Job
        fields = "__all__"
