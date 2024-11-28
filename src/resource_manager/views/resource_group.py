# Create your views here.
from common.views import CRUDView, CustomTableView
from resource_manager.forms import ResourceGroupForm
from resource_manager.models import ResourceGroup
from resource_manager.services import ResourceGroupService


# ------------------------------------------------------------------------------
# ResourceGroup VIEWS
# ------------------------------------------------------------------------------

RESOURCE_GROUP_MODEL_FIELDS = ["id", "name", "parent", "notes"]
RESOURCE_GROUP_SEARCH_FIELDS = ["name", "id", "notes"]

RESOURCE_GROUP_MODEL_RELATION_HEADERS = ["Resources", "History"]
RESOURCE_GROUP_MODEL_RELATION_FIELDS = {
    "resources": {
        "model_name": "resources",
        "related_name": "resources",
        "fields": ["id", "name", "resource_type", "weekly_shift_template"],
        "headers": ["ID", "Resource Name", "Resource Type", "Weekly Shift Template"],
        "show_edit_actions": False,
    },
    "history": {
        "model_name": "history",
        "related_name": "history",
        "fields": ["history_id", "history_date", "history_type", "history_user"],
        "headers": ["ID", "History Date", "History Type", "History User"],
        "show_edit_actions": False,
    },
}

RESOURCE_GROUP_TABLE_VIEWS = CustomTableView(
    model=ResourceGroup,
    model_name="resource_group",
    fields=RESOURCE_GROUP_MODEL_FIELDS,
    model_relation_headers=RESOURCE_GROUP_MODEL_RELATION_HEADERS,
    model_relation_fields=RESOURCE_GROUP_MODEL_RELATION_FIELDS,
    search_fields_list=RESOURCE_GROUP_SEARCH_FIELDS,
)

RESOURCE_GROUP_VIEWS = CRUDView(
    model=ResourceGroup,
    model_name="resource_groups",
    model_service=ResourceGroupService,
    model_form=ResourceGroupForm,
    model_table_view=RESOURCE_GROUP_TABLE_VIEWS,
)
