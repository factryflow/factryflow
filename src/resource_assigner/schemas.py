from ninja import Field, ModelSchema

from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    AssignmentConstraint,
    TaskResourceAssigment,
    TaskRuleAssignment,
)


# ------------------------------------------------------------------
# AssignmentConstraint Schemas
# ------------------------------------------------------------------


class AssignmentConstraintBaseIn(ModelSchema):
    class Meta:
        model = AssignmentConstraint
        fields = [
            "resource_group",
            "resources",
            "resource_count",
            "use_all_resources",
            "custom_fields",
        ]


class AssignmentConstraintIn(AssignmentConstraintBaseIn):
    class Meta:
        model = AssignmentConstraint
        fields = AssignmentConstraintBaseIn.Meta.fields + [
            "task",
            "assignment_rule",
        ]


class AssignmentConstraintOut(ModelSchema):
    class Meta:
        model = AssignmentConstraint
        fields = "__all__"


# ------------------------------------------------------------------
# AssigmentRuleCriteria Schemas
# ------------------------------------------------------------------


class AssigmentRuleCriteriaBaseIn(ModelSchema):
    class Meta:
        model = AssigmentRuleCriteria
        fields = ["operator", "field", "value", "custom_fields"]


class AssigmentRuleCriteriaIn(AssigmentRuleCriteriaBaseIn):
    class Meta:
        model = AssigmentRuleCriteria
        fields = AssigmentRuleCriteriaBaseIn.Meta.fields + ["assigment_rule"]


class AssigmentRuleCriteriaOut(ModelSchema):
    class Meta:
        model = AssigmentRuleCriteria
        fields = "__all__"


# ------------------------------------------------------------------
# AssigmentRule Schemas
# ------------------------------------------------------------------


class AssigmentRuleIn(ModelSchema):
    criteria: list[AssigmentRuleCriteriaBaseIn] = None
    assignment_constraints: list[AssignmentConstraintBaseIn] = None

    class Meta:
        model = AssigmentRule
        fields = [
            "name",
            "description",
            "notes",
            "external_id",
            "work_center",
            "is_active",
            "custom_fields",
        ]


class AssigmentRuleOut(ModelSchema):
    class Meta:
        model = AssigmentRule
        fields = "__all__"


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
