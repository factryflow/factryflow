from ninja import Field, ModelSchema, Schema

from resource_calendar.models import (
    OperationalException,
    OperationalExceptionType,
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
)

from .utils import TIME_24HR_PATTERN


# ------------------------------------------------------------------------------
# WeeklyShiftTemplate Schemas
# ------------------------------------------------------------------------------


class WeeklyShiftTemplateDetailBase(Schema):
    day_of_week: str = Field(..., example="Monday", help_text="Day of the week")
    start_time: str = Field(
        ..., pattern=TIME_24HR_PATTERN, example="08:00", help_text="24 hour format"
    )
    end_time: str = Field(
        ..., pattern=TIME_24HR_PATTERN, example="16:00", help_text="24 hour format"
    )


class WeeklyShiftTemplateDetailIn(ModelSchema):
    class Meta:
        model = WeeklyShiftTemplateDetail
        fields = ["day_of_week", "start_time", "end_time", "weekly_shift_template"]


class WeeklyShiftTemplateDetailOut(ModelSchema):
    class Meta:
        model = WeeklyShiftTemplateDetail
        fields = "__all__"


# ------------------------------------------------------------------------------
# WeeklyShiftTemplate Schemas
# ------------------------------------------------------------------------------


class WeeklyShiftTemplateIn(ModelSchema):
    weekly_shift_template_details: list[WeeklyShiftTemplateDetailBase] = None

    class Meta:
        model = WeeklyShiftTemplate
        fields = ["name", "description", "external_id", "notes", "custom_fields"]


class WeeklyShiftTemplateOut(ModelSchema):
    class Meta:
        model = WeeklyShiftTemplate
        fields = "__all__"


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
