from common.views import CRUDView, CustomTableView

# Create your views here.
from resource_calendar.models import (
    WeeklyShiftTemplateDetail,
)
from resource_calendar.forms import WeeklyShiftTemplateDetailForm
from resource_calendar.services import WeeklyShiftTemplateDetailService


# ------------------------------------------------------------------------------
# Weekly Shift Template Detail VIEWS
# ------------------------------------------------------------------------------

WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_FIELDS = [
    "id",
    "day_of_week",
    "start_time",
    "end_time",
]
WEEKLY_SHIFT_TEMPLATE_DETAIL_SEARCH_FIELDS = [
    "day_of_week",
    "id",
    "notes",
    "weekly_shift_template",
]

WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_RELATION_HEADERS = ["HISTORY"]
WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_RELATION_FIELDS = {
    "history": {
        "related_name": "history",
        "model_name": "history",
        "headers": ["ID", "History Date", "History Type", "History User"],
        "fields": ["history_id", "history_date", "history_type", "history_user"],
    },
}

WEEKLY_SHIFT_TEMPLATE_DETAIL_TABLE_VIEWS = CustomTableView(
    model=WeeklyShiftTemplateDetail,
    model_name="weekly_shift_template_detail",
    fields=WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_FIELDS,
    model_relation_headers=WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_RELATION_HEADERS,
    model_relation_fields=WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_RELATION_FIELDS,
    search_fields_list=WEEKLY_SHIFT_TEMPLATE_DETAIL_SEARCH_FIELDS,
)

WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS = CRUDView(
    model=WeeklyShiftTemplateDetail,
    model_name="weekly_shift_template_details",
    model_service=WeeklyShiftTemplateDetailService,
    model_form=WeeklyShiftTemplateDetailForm,
    model_table_view=WEEKLY_SHIFT_TEMPLATE_DETAIL_TABLE_VIEWS,
    sub_model_relation=True,
)
