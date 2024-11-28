# Create your views here.
from common.views import CRUDView, CustomTableView
from resource_manager.forms import ResourceForm
from resource_manager.models import Resource, ResourceTypeChoices
from resource_manager.services import ResourceService


# ------------------------------------------------------------------------------
# Resource VIEWS
# ------------------------------------------------------------------------------

RESOURCE_TAILWIND_CLASSES = {
    "Machine": "bg-haxgreen text-[#3DAD99]",
    "Operator": "bg-haxred text-[#FF4D4F]",
}

RESOURCE_MODEL_FIELDS = [
    "id",
    "name",
    "resource_type",
    "weekly_shift_template",
]

RESOURCE_STATUS_FILTER_FIELD = "resource_type"
RESOURCE_SEARCH_FIELDS = ["name", "id", "notes", "weekly_shift_template"]

RESOURCE_MODEL_RELATION_HEADERS = ["HISTORY"]
RESOURCE_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "fields": ["history_id", "history_date", "history_type", "history_user"],
        "headers": ["ID", "History Date", "History Type", "History User"],
        "show_edit_actions": False,
    }
}

RESOURCE_TABLE_VIEWS = CustomTableView(
    model=Resource,
    model_name="resource",
    fields=RESOURCE_MODEL_FIELDS,
    status_choices_class=ResourceTypeChoices,
    model_relation_headers=RESOURCE_MODEL_RELATION_HEADERS,
    model_relation_fields=RESOURCE_MODEL_RELATION_FIELDS,
    status_filter_field=RESOURCE_STATUS_FILTER_FIELD,
    search_fields_list=RESOURCE_SEARCH_FIELDS,
    tailwind_classes=RESOURCE_TAILWIND_CLASSES,
)

RESOURCE_VIEWS = CRUDView(
    model=Resource,
    model_name="resources",
    model_service=ResourceService,
    model_form=ResourceForm,
    model_table_view=RESOURCE_TABLE_VIEWS,
)
