from django.shortcuts import render

# Create your views here.
from common.views import CRUDView, CustomTableView
from .forms import ResourceForm, ResourcePoolForm
from .models import Resource, ResourceTypeChoices, ResourcePool
from .services import ResourceService, ResourcePoolService


# ------------------------------------------------------------------------------
# Resource VIEWS
# ------------------------------------------------------------------------------

RESOURCE_TAILWIND_CLASSES = {
    "M": "bg-haxgreen text-[#3DAD99]",
    "O": "bg-haxred text-[#FF4D4F]",
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
    "Weekly Shift Template"
]

ResourceTableView = CustomTableView(
    model=Resource,
    model_name="resource",
    fields=RESOURCE_MODEL_FIELDS,
    status_choices_class=ResourceTypeChoices,
    headers=RESOURCE_TABLE_HEADERS,
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

RESOURCE_POOL_MODEL_FIELDS = ["id", "external_id", "notes", "name", "parent"]
RESOURCE_POOL_SEARCH_FIELDS = ["name", "id"]
RESOURCE_POOL_TABLE_HEADERS = ["ID", "External ID", "Notes", "Resource Pool Name", "Parent"]

ResourcePoolTableView = CustomTableView(
    model=ResourcePool,
    model_name="resource_pool",
    fields=RESOURCE_POOL_MODEL_FIELDS,
    headers=RESOURCE_POOL_TABLE_HEADERS,
    search_fields_list=RESOURCE_POOL_SEARCH_FIELDS,
)

RESOURCE_POOL_VIEWS = CRUDView(
    model=ResourcePool,
    model_name="resource_pool",
    model_service=ResourcePoolService,
    model_form=ResourcePoolForm,
    model_table_view=ResourcePoolTableView,
)