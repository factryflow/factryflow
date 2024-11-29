from ninja import ModelSchema

from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
)
from .constraints import AssignmentConstraintBaseIn

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
