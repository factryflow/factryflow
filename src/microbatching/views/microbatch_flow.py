from common.views import CRUDView, CustomTableView

# Create your views here.
from microbatching.forms.microbatch_flow import (
    MicrobatchFlowForm,
)
from microbatching.models.microbatch_flow import MicrobatchFlow
from microbatching.services.microbatch_flow import (
    MicrobatchFlowService,
)

# ------------------------------------------------------------------------------
# Microbatch Views
# ------------------------------------------------------------------------------

MICROBATCH_FLOW_MODEL_FIELDS = [
    "id",
    "name",
    "description",
    "work_center",
]
MICROBATCH_FLOW_TABLE_HEADERS = [
    "ID",
    "Name",
    "Description",
    "Work Center",
]

MICROBATCH_FLOW_SEARCH_FIELDS = ["name", "work_center"]

MICROBATCH_FLOW_MODEL_RELATION_HEADERS = [
    "HISTORY",
]

MICROBATCH_FLOW_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "History Date", "History Type", "History User"],
        "fields": ["history_id", "history_date", "history_type", "history_user"],
        "show_edit_actions": False,
    },
}

MICROBATCH_FLOW_TABLE_VIEW = CustomTableView(
    model=MicrobatchFlow,
    model_name="microbatch_flow",
    fields=MICROBATCH_FLOW_MODEL_FIELDS,
    headers=MICROBATCH_FLOW_TABLE_HEADERS,
    model_relation_headers=MICROBATCH_FLOW_MODEL_RELATION_HEADERS,
    model_relation_fields=MICROBATCH_FLOW_MODEL_RELATION_FIELDS,
    search_fields_list=MICROBATCH_FLOW_SEARCH_FIELDS,
)

MICROBATCH_FLOW_VIEWS = CRUDView(
    model=MicrobatchFlow,
    model_name="microbatch_flows",
    model_service=MicrobatchFlowService,
    model_form=MicrobatchFlowForm,
    model_table_view=MICROBATCH_FLOW_TABLE_VIEW,
)
