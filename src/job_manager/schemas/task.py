from ninja import Field, ModelSchema, Schema

from job_manager.models import Task, TaskStatusChoices, TaskType, WorkCenter
from resource_assigner.schemas import AssignmentConstraintBaseIn

# ------------------------------------------------------------------
# WorkCenter Schemas
# ------------------------------------------------------------------


class WorkCenterIn(ModelSchema):
    class Meta:
        model = WorkCenter
        fields = ["name", "external_id", "notes", "custom_fields"]


class WorkCenterOut(ModelSchema):
    class Meta:
        model = WorkCenter
        fields = "__all__"


# ------------------------------------------------------------------
# TaskType Schemas
# ------------------------------------------------------------------


class TaskTypeIn(ModelSchema):
    class Meta:
        model = TaskType
        fields = ["name", "external_id", "notes", "custom_fields"]


class TaskTypeOut(ModelSchema):
    class Meta:
        model = TaskType
        fields = "__all__"


# ------------------------------------------------------------------
# Task Schemas
# ------------------------------------------------------------------


class TaskIn(ModelSchema):
    predecessors: list[int] = Field(None)
    dependencies: list[int] = Field(None)
    task_status: TaskStatusChoices = Field(None)

    class Meta:
        model = Task
        exclude = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "planned_start_datetime",
            "planned_end_datetime",
        ]


class TaskOut(ModelSchema):
    class Meta:
        model = Task
        fields = "__all__"
