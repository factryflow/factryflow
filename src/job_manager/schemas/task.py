from ninja import Field, ModelSchema

from job_manager.models import (
    Task,
    TaskType,
    TaskStatusChoices
)


class TaskTypeIn(ModelSchema):
    class Meta:
        model = TaskType
        fields = ["name"]


class TaskTypeOut(ModelSchema):
    class Meta:
        model = TaskType
        fields = "__all__"


class TaskIn(ModelSchema):
    predecessors: list[int] = Field(None, alias="predecessor_ids")
    dependencies: list[int] = Field(None, alias="dependency_ids")
    task_status: TaskStatusChoices = Field(None, alias="taskStatus")

    class Meta:
        model = Task
        fields = [
            "name",
            "id",
            "external_id",
            "planned_start_datetime",
            "planned_end_datetime",
            "setup_time",
            "run_time_per_unit",
            "teardown_time",
            "quantity",
            "item",
            "work_center",
            "job",
            "task_type",
        ]


class TaskOut(ModelSchema):
    class Meta:
        model = Task
        fields = "__all__"
