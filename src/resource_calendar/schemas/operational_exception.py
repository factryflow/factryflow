from ninja import ModelSchema
from resource_calendar.models import (
    OperationalException,
    OperationalExceptionType,
)


# ------------------------------------------------------------------------------
# OperationalExceptionType Schemas
# ------------------------------------------------------------------------------


class OperationalExceptionTypeIn(ModelSchema):
    class Meta:
        model = OperationalExceptionType
        fields = ["name", "external_id", "notes", "custom_fields"]


class OperationalExceptionTypeOut(ModelSchema):
    class Meta:
        model = OperationalExceptionType
        fields = "__all__"


# ------------------------------------------------------------------------------
# OperationalException Schemas
# ------------------------------------------------------------------------------


class OperationalExceptionIn(ModelSchema):
    class Meta:
        model = OperationalException
        fields = [
            "external_id",
            "start_datetime",
            "end_datetime",
            "operational_exception_type",
            "weekly_shift_template",
            "resource",
            "notes",
            "custom_fields",
        ]


class OperationalExceptionOut(ModelSchema):
    class Meta:
        model = OperationalException
        fields = "__all__"
