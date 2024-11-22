from ninja import Field, ModelSchema

from microbatching.models.microbatch_rule import MicrobatchRule, MicrobatchRuleCriteria


# --------------------------------------------------------------------
# MicrobatchRuleCriteria Schemas
# --------------------------------------------------------------------


class MicrobatchRuleCriteriaBaseIn(ModelSchema):
    # Schema for MicrobatchRuleCriteria input
    class Meta:
        model = MicrobatchRuleCriteria
        fields = ["field", "operator", "value"]


class MicrobatchRuleCriteriaIn(MicrobatchRuleCriteriaBaseIn):
    # Schema for MicrobatchRuleCriteria input
    class Meta:
        model = MicrobatchRuleCriteria
        fields = MicrobatchRuleCriteriaBaseIn.Meta.fields + ["custom_fields"]


class MicrobatchRuleCriteriaOut(ModelSchema):
    # Schema for MicrobatchRuleCriteria output
    class Meta:
        model = MicrobatchRuleCriteria
        fields = "__all__"


# --------------------------------------------------------------------
# MicrobatchRule Schemas
# --------------------------------------------------------------------


class MicrobatchRuleIn(ModelSchema):
    # Schema for MicrobatchRule input
    criteria: list[MicrobatchRuleCriteriaBaseIn] = Field(None)

    class Meta:
        model = MicrobatchRule
        fields = [
            "name",
            "external_id",
            "notes",
            "is_active",
            "custom_fields",
        ]


class MicrobatchRuleOut(ModelSchema):
    # Schema for MicrobatchRule output
    class Meta:
        model = MicrobatchRule
        fields = "__all__"
