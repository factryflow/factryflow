from ninja import ModelSchema

from resource_assigner.models import AssignmentConstraint


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
