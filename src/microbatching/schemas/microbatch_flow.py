from ninja import Field, ModelSchema

from microbatching.models.microbatch_flow import MicrobatchFlow


# --------------------------------------------------------------------
# MicrobatchFlow Schemas
# --------------------------------------------------------------------


class MicrobatchFlowIn(ModelSchema):
    # Schema for MicrobatchFlow input
    class Meta:
        model = MicrobatchFlow
        fields = [
            "name",
            "description",
            "start_rule",
            "end_rule",
            "min_flow_length",
            "max_flow_length",
            "custom_fields",
        ]


class MicrobatchFlowOut(ModelSchema):
    # Schema for MicrobatchFlow output
    class Meta:
        model = MicrobatchFlow
        fields = "__all__"
