from common.views import CRUDView, CustomTableView

# Create your views here.
from microbatching.forms import (
    MicrobatchRuleForm,
)
from microbatching.models import (
    MicrobatchRule,
)
from microbatching.services import (
    MicrobatchRuleService,
)

# ------------------------------------------------------------------------------
# Microbatch Views
# ------------------------------------------------------------------------------

MICROBATCH_RULE_MODEL_FIELDS = [
    "id",
    "item_name",
    "work_center",
    "batch_size",
]
MICROBATCH_RULE_TABLE_HEADERS = [
    "Id",
    "Item Name",
    "Work Center",
    "Batch Size",
]

MICROBATCH_RULE_SEARCH_FIELDS = ["item_name", "work_center", "batch_size"]

MICROBATCH_RULE_MODEL_RELATION_HEADERS = [
    "HISTORY",
]

MICROBATCH_RULE_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "History Date", "History Type", "History User"],
        "fields": ["history_id", "history_date", "history_type", "history_user"],
        "show_edit_actions": False,
    },
}

MICROBATCH_RULE_TABLE_VIEW = CustomTableView(
    model=MicrobatchRule,
    model_name="microbatch_rule",
    fields=MICROBATCH_RULE_MODEL_FIELDS,
    headers=MICROBATCH_RULE_TABLE_HEADERS,
    model_relation_headers=MICROBATCH_RULE_MODEL_RELATION_HEADERS,
    model_relation_fields=MICROBATCH_RULE_MODEL_RELATION_FIELDS,
    search_fields_list=MICROBATCH_RULE_SEARCH_FIELDS,
)

MICROBATCH_RULE_VIEWS = CRUDView(
    model=MicrobatchRule,
    model_name="microbatch_rules",
    model_service=MicrobatchRuleService,
    model_form=MicrobatchRuleForm,
    model_table_view=MICROBATCH_RULE_TABLE_VIEW,
)
