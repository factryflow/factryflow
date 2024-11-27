from ninja import ModelSchema

from resource_calendar.models import WeeklyShiftTemplate
from .shift_template_detail import WeeklyShiftTemplateDetailBase


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
