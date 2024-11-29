from ninja import ModelSchema

from resource_assigner.models import (
    TaskResourceAssigment,
    TaskRuleAssignment,
)

# ------------------------------------------------------------------
# TaskResourceAssigment Schemas
# ------------------------------------------------------------------


class TaskResourceAssigmentIn(ModelSchema):
    class Meta:
        model = TaskResourceAssigment
        fields = ["task", "resources", "custom_fields"]


class TaskResourceAssigmentOut(ModelSchema):
    class Meta:
        model = TaskResourceAssigment
        fields = "__all__"


# ------------------------------------------------------------------
# TaskRuleAssignment Schemas
# ------------------------------------------------------------------


class TaskRuleAssignmentIn(ModelSchema):
    class Meta:
        model = TaskRuleAssignment
        fields = ["task", "assigment_rule", "is_applied", "custom_fields"]


class TaskRuleAssignmentOut(ModelSchema):
    class Meta:
        model = TaskRuleAssignment
        fields = "__all__"
