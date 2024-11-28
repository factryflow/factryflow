# views.py
from common.views import CRUDView, CustomTableView

from job_manager.forms import (
    DependencyForm,
    DependencyTypeForm,
)
from job_manager.models import (
    Dependency,
    DependencyStatusChoices,
    DependencyType,
    Job,
    Task,
)
from job_manager.services import (
    DependencyService,
    DependencyTypeService,
)


# ------------------------------------------------------------------------------
# Dependecy Type Views
# ------------------------------------------------------------------------------

DEPENDENCY_TYPE_MODEL_FIELDS = ["id", "name", "notes"]

DEPENDENCY_TYPE_SEARCH_FIELDS = ["name", "notes", "id"]

DEPENDENCY_TYPE_MODEL_RELATION_HEADERS = ["HISTORY"]
DEPENDENCY_TYPE_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "Name", "User", "Notes", "History Date"],
        "fields": ["history_id", "name", "history_user", "notes", "history_date"],
        "show_edit_actions": False,
    },
}

DEPENDENCY_TYPE_TABLE_VIEW = CustomTableView(
    model=DependencyType,
    model_name="dependency_type",
    fields=DEPENDENCY_TYPE_MODEL_FIELDS,
    model_relation_headers=DEPENDENCY_TYPE_MODEL_RELATION_HEADERS,
    model_relation_fields=DEPENDENCY_TYPE_MODEL_RELATION_FIELDS,
    search_fields_list=DEPENDENCY_TYPE_SEARCH_FIELDS,
)

DEPENDENCY_TYPE_VIEWS = CRUDView(
    model=DependencyType,
    model_name="dependency_types",
    model_service=DependencyTypeService,
    model_form=DependencyTypeForm,
    model_table_view=DEPENDENCY_TYPE_TABLE_VIEW,
)


# ------------------------------------------------------------------------------
# Dependecy Views
# ------------------------------------------------------------------------------

DEPENDENCY_MODEL_FIELDS = [
    "id",
    "name",
    "expected_close_datetime",
    "actual_close_datetime",
    "dependency_type",
    "dependency_status",
]

DEPENDENCY_TAILWIND_CLASSES = {
    "PD": "bg-haxred text-[#FF4D4F]",
    "IP": "bg-haxyellow text-[#F6C000]",
    "RS": "bg-haxgreen text-[#3DAD99]",
    "CN": "bg-haxpurple text-[#7239EA]",
}

DEPENDENCY_STATUS_FILTER_FIELD = "dependency_status"
DEPENDENCY_SEARCH_FIELDS = ["name", "id", "dependency_type", "notes"]

DEPENDENCY_MODEL_RELATION_HEADERS = ["TASKS", "JOBS", "HISTORY"]

DEPENDENCY_MODEL_RELATION_FIELDS = {
    "tasks": {
        "model": Task,
        "model_name": "task",
        "related_name": "dependencies",
        "headers": [
            "ID",
            "Task Name",
            "Item",
            "Quantity",
            "Run Time",
            "Planned Start",
            "Planned End",
            "Task Type",
            "Status",
        ],
        "fields": [
            "id",
            "name",
            "item",
            "quantity",
            "run_time_per_unit",
            "planned_start_datetime",
            "planned_end_datetime",
            "task_type",
            "task_status",
        ],
        "show_edit_actions": False,
    },
    "jobs": {
        "model": Job,
        "model_name": "job",
        "related_name": "dependencies",
        "headers": [
            "ID",
            "Job Name",
            "Description",
            "Customer",
            "Due Date",
            "Planned Start",
            "Planned End",
            "Priority",
            "Status",
        ],
        "fields": [
            "id",
            "name",
            "description",
            "customer",
            "due_date",
            "planned_start_datetime",
            "planned_end_datetime",
            "priority",
            "job_status",
        ],
        "show_edit_actions": False,
    },
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": [
            "ID",
            "Name",
            "User",
            "Expected Close",
            "Actual Close",
            "Type",
            "Status",
            "Notes",
            "History Date",
        ],
        "fields": [
            "history_id",
            "name",
            "history_user",
            "expected_close_datetime",
            "actual_close_datetime",
            "dependency_type",
            "dependency_status",
            "notes",
            "history_date",
        ],
        "show_edit_actions": False,
    },
}

DEPENDENCY_TABLE_VIEW = CustomTableView(
    model=Dependency,
    model_name="dependencies",
    fields=DEPENDENCY_MODEL_FIELDS,
    status_choices_class=DependencyStatusChoices,
    model_relation_fields=DEPENDENCY_MODEL_RELATION_FIELDS,
    model_relation_headers=DEPENDENCY_MODEL_RELATION_HEADERS,
    status_filter_field=DEPENDENCY_STATUS_FILTER_FIELD,
    search_fields_list=DEPENDENCY_SEARCH_FIELDS,
    tailwind_classes=DEPENDENCY_TAILWIND_CLASSES,
)

DEPENDENCY_VIEWS = CRUDView(
    model=Dependency,
    model_type=DependencyType,
    model_name="dependencies",
    model_service=DependencyService,
    model_form=DependencyForm,
    model_table_view=DEPENDENCY_TABLE_VIEW,
)
