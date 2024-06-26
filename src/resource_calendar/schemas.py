from ninja import Field, ModelSchema, Schema

from resource_calendar.models import (
    OperationalException,
    OperationalExceptionType,
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
)

from .utils import TIME_24HR_PATTERN


class WeeklyShiftTemplateDetailIn(Schema):
    day_of_week: int = Field(
        ..., ge=0, le=6, example=0, help_text="0 is Monday, 6 is Sunday"
    )
    start_time: str = Field(
        ..., pattern=TIME_24HR_PATTERN, example="08:00", help_text="24 hour format"
    )
    end_time: str = Field(
        ..., pattern=TIME_24HR_PATTERN, example="16:00", help_text="24 hour format"
    )


class WeeklyShiftTemplateDetailOut(ModelSchema):
    class Meta:
        model = WeeklyShiftTemplateDetail
        fields = "__all__"


class WeeklyShiftTemplateIn(Schema):
    name: str = Field(..., example="Day Shift")
    details: list[WeeklyShiftTemplateDetailIn] = None

    class Meta:
        model = WeeklyShiftTemplate
        fields = ["name", "external_id", "notes"]


class WeeklyShiftTemplateOut(ModelSchema):
    details: list[WeeklyShiftTemplateDetailOut] = []

    class Meta:
        model = WeeklyShiftTemplate
        fields = "__all__"


class OperationalExceptionTypeIn(ModelSchema):
    class Meta:
        model = OperationalExceptionType
        fields = ["name", "external_id", "notes"]


class OperationalExceptionTypeOut(ModelSchema):
    class Meta:
        model = OperationalExceptionType
        fields = "__all__"


class OperationalExceptionIn(ModelSchema):
    class Meta:
        model = OperationalException
        fields = [
            "external_id",
            "start_datetime",
            "end_datetime",
            "operational_exception_type",
            "notes",
        ]


class OperationalExceptionOut(ModelSchema):
    class Meta:
        model = OperationalException
        fields = "__all__"
