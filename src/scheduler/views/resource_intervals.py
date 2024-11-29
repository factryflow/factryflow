from common.views import CRUDView, CustomTableView

# Create your views here.
from scheduler.models import ResourceIntervals
from scheduler.forms import ResourceIntervalsForm
from scheduler.services import ResourceIntervalsService


# ------------------------------------------------------------------------------
# Resource Intervals VIEWS
# ------------------------------------------------------------------------------


RESOURCE_INTERVALS_MODEL_FIELDS = [
    "resource",
    "task",
    "interval_start",
    "interval_end",
]

RESOURCE_INTERVALS_SEARCH_FIELDS = ["resource", "task"]

RESOURCE_INTERVALS_MODELS_RELATION_HEADERS = ["HISTORY"]

RESOURCE_INTERVALS_MODELS_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": [
            "ID",
            "Resource",
            "Task",
            "Interval Start",
            "Interval End",
            "History Date",
            "History Type",
            "History User",
        ],
        "fields": [
            "history_id",
            "resource",
            "task",
            "interval_start",
            "interval_end",
            "history_date",
            "history_type",
            "history_user",
        ],
        "show_edit_actions": False,
    },
}

RESOURCE_INTERVAL_TABLE_VIEW = CustomTableView(
    model=ResourceIntervals,
    model_name="resource_intervals",
    fields=RESOURCE_INTERVALS_MODEL_FIELDS,
    model_relation_headers=RESOURCE_INTERVALS_MODELS_RELATION_HEADERS,
    model_relation_fields=RESOURCE_INTERVALS_MODELS_RELATION_FIELDS,
    search_fields_list=RESOURCE_INTERVALS_SEARCH_FIELDS,
)


RESOURCE_INTERVAL_VIEW = CRUDView(
    model=ResourceIntervals,
    model_name="resource_intervals",
    model_form=ResourceIntervalsForm,
    model_service=ResourceIntervalsService,
    model_table_view=RESOURCE_INTERVAL_TABLE_VIEW,
    user_rule_permission=False,
)
