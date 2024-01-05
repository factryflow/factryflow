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


class AssigmentRuleCriteriaIn(ModelSchema):
    id: int = Field(None)
    operator: Operator = Field(None, alias="operator")

    class Meta:
        model = AssigmentRuleCriteria
        fields = ["field", "value"]


class AssigmentRuleCriteriaOut(ModelSchema):
    class Meta:
        model = AssigmentRuleCriteria
        fields = "__all__"


class AssigmentRuleIn(ModelSchema):
    resource_group_id: int
    work_center_id: int
    criteria: list[AssigmentRuleCriteriaIn] = Field(None)

    class Meta:
        model = AssigmentRule
        fields = ["name", "description"]


class AssigmentRuleOut(ModelSchema):
    resource_group_id: int
    work_center_id: int
    criteria: list[AssigmentRuleCriteriaOut] = Field([])

    class Meta:
        model = AssigmentRule
        exclude = ["resource_group", "work_center"]
