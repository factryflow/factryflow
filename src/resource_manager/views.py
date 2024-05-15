# Create your views here.
from common.views import CRUDView, CustomTableView
from .forms import *
from .models import *
from .services import *


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
RESOURCE_SEARCH_FIELDS = ["name", "id"]
RESOURCE_TABLE_HEADERS = [
    "ID",
    "Resource Name",
    "Resource Type",
    "Weekly Shift Template",
]

RESOURCE_MODEL_RELATION_HEADERS = ["HISTORY"]
RESOURCE_MODEL_RELATION_FIELDS = {
    "history": [
        "history",
        ["ID", "History Date", "History Type", "History User"],
        ["id", "history_date", "history_type", "history_user"],
    ],
}

ResourceTableView = CustomTableView(
    model=Resource,
    model_name="resource",
    fields=RESOURCE_MODEL_FIELDS,
    status_choices_class=ResourceTypeChoices,
    headers=RESOURCE_TABLE_HEADERS,
    model_relation_headers=RESOURCE_MODEL_RELATION_HEADERS,
    model_relation_fields=RESOURCE_MODEL_RELATION_FIELDS,
    status_filter_field=RESOURCE_STATUS_FILTER_FIELD,
    search_fields_list=RESOURCE_SEARCH_FIELDS,
    tailwind_classes=RESOURCE_TAILWIND_CLASSES,
)

RESOURCE_VIEWS = CRUDView(
    model=Resource,
    model_name="resource",
    model_service=ResourceService,
    model_form=ResourceForm,
    model_table_view=ResourceTableView,
)


# ------------------------------------------------------------------------------
# ResourcePool VIEWS
# ------------------------------------------------------------------------------

RESOURCE_Group_MODEL_FIELDS = ["id", "external_id", "notes", "name", "parent"]
RESOURCE_Group_SEARCH_FIELDS = ["name", "id"]
RESOURCE_Group_TABLE_HEADERS = [
    "ID",
    "External ID",
    "Notes",
    "Resource Group Name",
    "Parent",
]


RESOURCE_Group_MODEL_RELATION_HEADERS = ["Resources", "Work Units"]
RESOURCE_Group_MODEL_RELATION_FIELDS = {
    "resources": [
        "resources",
        ["ID", "Resource Name", "Resource Type", "Weekly Shift Template"],
        ["id", "name", "resource_type", "weekly_shift_template"],
    ],
}

ResourceGroupTableView = CustomTableView(
    model=ResourceGroup,
    model_name="resource_group",
    fields=RESOURCE_Group_MODEL_FIELDS,
    model_relation_headers=RESOURCE_Group_MODEL_RELATION_HEADERS,
    model_relation_fields=RESOURCE_Group_MODEL_RELATION_FIELDS,
    headers=RESOURCE_Group_TABLE_HEADERS,
    search_fields_list=RESOURCE_Group_SEARCH_FIELDS,
)

RESOURCE_GROUP_VIEWS = CRUDView(
    model=ResourceGroup,
    model_name="resource_pool",
    model_service=ResourceGroupService,
    model_form=ResourceGroupForm,
    model_table_view=ResourceGroupTableView,
)
