from common.views import CRUDView, CustomTableView

# Create your views here.
from resource_calendar.models import (
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
    DaysOfWeek,
)
from resource_calendar.forms import WeeklyShiftTemplateDetailForm, WeeklyShiftTemplateForm
from resource_calendar.services import WeeklyShiftTemplateService


# ------------------------------------------------------------------------------
# Weekly Shift Template VIEWS
# ------------------------------------------------------------------------------

WEEKLY_SHIFT_TEMPLATE_MODEL_FIELDS = ["id", "name", "notes"]
WEEKLY_SHIFT_TEMPLATE_SEARCH_FIELDS = ["name", "id", "notes"]

WEEKLY_SHIFT_TEMPLATE_MODEL_RELATION_HEADERS = [
    "TEMPLATE DETAILS",
    "HISTORY",
]

WEEKLY_SHIFT_TEMPLATE_MODEL_RELATION_FIELDS = {
    "template_details": {
        "related_name": "weekly_shift_template_details",
        "model_name": "weekly_shift_template_detail",
        "headers": ["ID", "Day of Week", "Start Time", "End Time"],
        "fields": ["id", "day_of_week", "start_time", "end_time"],
        "select_fields": {
            "day_of_week": dict(DaysOfWeek.choices),
        },
        "relationship_fields": "weekly_shift_template",
        "show_edit_actions": True,
    },
    "history": {
        "related_name": "history",
        "model_name": "history",
        "headers": ["ID", "History Date", "History Type", "History User"],
        "fields": ["history_id", "history_date", "history_type", "history_user"],
        "show_edit_actions": False,
    },
}

SHIFT_TEMPLATE_DETAILS_FORMSET_FORM_FIELDS = ["day_of_week", "start_time", "end_time"]

SHIFT_TEMPLATE_DETAILS_FORMSET_OPTIONS = [
    WeeklyShiftTemplateDetail,
    WeeklyShiftTemplateDetailForm,
    "weekly_shift_template_details",
    SHIFT_TEMPLATE_DETAILS_FORMSET_FORM_FIELDS,
    "weekly_shift_template_details",
]


WEEKLY_SHIFT_TEMPLATE_TABLE_VIEWS = CustomTableView(
    model=WeeklyShiftTemplate,
    model_name="weekly_shift_template",
    fields=WEEKLY_SHIFT_TEMPLATE_MODEL_FIELDS,
    search_fields_list=WEEKLY_SHIFT_TEMPLATE_SEARCH_FIELDS,
    model_relation_headers=WEEKLY_SHIFT_TEMPLATE_MODEL_RELATION_HEADERS,
    model_relation_fields=WEEKLY_SHIFT_TEMPLATE_MODEL_RELATION_FIELDS,
)

WEEKLY_SHIFT_TEMPLATE_VIEWS = CRUDView(
    model=WeeklyShiftTemplate,
    model_name="weekly_shift_templates",
    model_service=WeeklyShiftTemplateService,
    model_form=WeeklyShiftTemplateForm,
    model_table_view=WEEKLY_SHIFT_TEMPLATE_TABLE_VIEWS,
    formset_options=SHIFT_TEMPLATE_DETAILS_FORMSET_OPTIONS,
)