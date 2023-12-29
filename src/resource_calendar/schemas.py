from ninja import ModelSchema

from resource_calendar.models import (
    OperationalException,
    OperationalExceptionType,
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
)


class WeeklyShiftTemplateIn(ModelSchema):
    class Meta:
        model = WeeklyShiftTemplate
        fields = ["name"]


class WeeklyShiftTemplateOut(ModelSchema):
    class Meta:
        model = WeeklyShiftTemplate
        fields = "__all__"


class WeeklyShiftTemplateDetailIn(ModelSchema):
    class Meta:
        model = WeeklyShiftTemplateDetail
        fields = [
            "weekly_shift_template",
            "day_of_week",
            "start_time",
            "end_time",
        ]


class WeeklyShiftTemplateDetailOut(ModelSchema):
    class Meta:
        model = WeeklyShiftTemplateDetail
        fields = "__all__"


class OperationalExceptionTypeIn(ModelSchema):
    class Meta:
        model = OperationalExceptionType
        fields = ["name"]


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
