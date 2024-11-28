from ninja import Field, ModelSchema, Schema

from resource_calendar.models import (
    WeeklyShiftTemplateDetail,
)

from resource_calendar.utils import TIME_24HR_PATTERN


# ------------------------------------------------------------------------------
# WeeklyShiftTemplateDetail Schemas
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
