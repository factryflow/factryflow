from ninja import Field, ModelSchema

from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    AssignmentConstraint,
    Operator,
)


class AssignmentConstraintIn(ModelSchema):
    resources: list[int] = Field(None, alias="resource_ids")
    work_units: list[int] = Field(None, alias="work_unit_ids")

    class Meta:
        model = AssignmentConstraint
        fields = [
            "task",
            "assignment_rule",
            "resource_pool",
            "required_units",
            "is_direct",
        ]


class AssignmentConstraintOut(ModelSchema):
    resource_ids: list[int] = Field([], alias="resource_id_list")
    work_unit_ids: list[int] = Field([], alias="work_unit_id_list")

    class Meta:
        model = AssignmentConstraint
        exclude = ["resources", "work_units"]


class AssigmentRuleCriteriaIn(ModelSchema):
    operator: Operator

    class Meta:
        model = AssigmentRuleCriteria
        fields = ["field", "value"]


class AssigmentRuleCriteriaOut(ModelSchema):
    class Meta:
        model = AssigmentRuleCriteria
        fields = "__all__"


class AssigmentRuleIn(ModelSchema):
    work_center_id: int
    criteria: list[AssigmentRuleCriteriaIn] = None
    assignment_constraints: list[AssignmentConstraintIn] = None

    class Meta:
        model = AssigmentRule
        fields = ["name", "description", "notes", "external_id"]


class AssigmentRuleOut(ModelSchema):
    work_center_id: int
    criteria: list[AssigmentRuleCriteriaOut] = []
    assignment_constraints: list[AssignmentConstraintOut] = []

    class Meta:
        model = AssigmentRule
        exclude = ["work_center"]
