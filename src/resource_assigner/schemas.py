from ninja import Field, ModelSchema

from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    AssignmentConstraint,
    Operator,
)


class AssignmentConstraintIn(ModelSchema):
    resources: list[int] = Field(None, alias="resource_ids")

    class Meta:
        model = AssignmentConstraint
        fields = [
            "task",
            "assignment_rule",
            "resource_group",
            "resources",
            "resource_count",
            "use_all_resources",
        ]


class AssignmentConstraintOut(ModelSchema):
    resource_ids: list[int] = Field([], alias="resource_id_list")

    class Meta:
        model = AssignmentConstraint
        exclude = ["resources"]


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
