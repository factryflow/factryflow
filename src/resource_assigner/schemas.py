from ninja import Field, ModelSchema

from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    Operator,
    TaskResourceAssigment,
)


class TaskResourceAssigmentIn(ModelSchema):
    resources: list[int] = Field(None, alias="resource_ids")

    class Meta:
        model = TaskResourceAssigment
        fields = [
            "task",
            "resource_group",
            "resource_count",
            "use_all_resources",
            "is_direct",
        ]


class TaskResourceAssigmentOut(ModelSchema):
    resource_ids: list[int] = Field([], alias="resource_id_list")

    class Meta:
        model = TaskResourceAssigment
        exclude = ["resources"]


class AssigmentRuleIn(ModelSchema):
    class Meta:
        model = AssigmentRule
        fields = ["name", "description", "resource_group", "work_center"]


class AssigmentRuleOut(ModelSchema):
    class Meta:
        model = AssigmentRule
        fields = "__all__"


class AssigmentRuleCriteriaIn(ModelSchema):
    operator: Operator = Field(None, alias="operator")

    class Meta:
        model = AssigmentRuleCriteria
        fields = ["field", "value", "assigment_rule"]


class AssigmentRuleCriteriaOut(ModelSchema):
    operator: Operator = Field(None, alias="operator")

    class Meta:
        model = AssigmentRuleCriteria
        fields = "__all__"
        exclude = ["operator"]
