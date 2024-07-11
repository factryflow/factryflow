# views.py

from common.views import CRUDView, CustomTableView

from .forms import (
    DependencyForm,
    DependencyTypeForm,
    ItemForm,
    JobForm,
    TaskForm,
    TaskTypeForm,
    WorkCenterForm,
    JobTypeForm,
)
from .models import (
    Dependency,
    DependencyType,
    Item,
    Job,
    Task,
    TaskType,
    WorkCenter,
    JobType,
    TaskStatusChoices,
    JobStatusChoices,
    DependencyStatusChoices,
)
from .services import (
    DependencyService,
    DependencyTypeService,
    ItemService,
    JobService,
    TaskService,
    TaskTypeService,
    WorkCenterService,
    JobTypeService,
)

from resource_assigner.models import TaskRuleAssignment


# ------------------------------------------------------------------------------
# WorkCenter Views
# ------------------------------------------------------------------------------

WORK_CENTER_MODEL_FIELDS = ["id", "name", "external_id", "notes"]
WORK_CENTER_SEARCH_FIELDS = ["name", "id"]
WORK_CENTER_TABLE_HEADERS = ["ID", "Work Center Name", "External ID", "Notes"]

WORK_CENTER_MODEL_RELATION_HEADERS = ["HISTORY"]
WORK_CENTER_FIELD_MODEL_RELATION_FIELDS = {
    "history": [
        "history",
        ["ID", "External ID", "Name", "User", "Notes", "History Date"],
        ["id", "external_id", "name", "history_user", "notes", "history_date"],
    ],
}

WorkCenterTableView = CustomTableView(
    model=WorkCenter,
    model_name="work_center",
    fields=WORK_CENTER_MODEL_FIELDS,
    headers=WORK_CENTER_TABLE_HEADERS,
    model_relation_headers=WORK_CENTER_MODEL_RELATION_HEADERS,
    model_relation_fields=WORK_CENTER_FIELD_MODEL_RELATION_FIELDS,
    search_fields_list=WORK_CENTER_SEARCH_FIELDS,
)

WORK_CENTER_VIEWS = CRUDView(
    model=WorkCenter,
    model_name="work_center",
    model_service=WorkCenterService,
    model_form=WorkCenterForm,
    model_table_view=WorkCenterTableView,
)


# ------------------------------------------------------------------------------
# Job Type Views
# ------------------------------------------------------------------------------

JOB_TYPE_MODEL_FIELDS = ["id", "external_id", "name", "notes"]

JOB_TYPE_TABLE_HEADERS = ["ID", "External ID", "Job Type Name", "Notes"]
JOB_TYPE_SEARCH_FIELDS = ["name", "notes", "external_id"]

JOB_TYPE_MODEL_RELATION_HEADERS = ["HISTORY"]
JOB_TYPE_MODEL_RELATION_FIELDS = {
    "history": [
        "history",
        ["ID", "External ID", "Name", "User", "Notes", "History Date"],
        ["id", "external_id", "name", "history_user", "notes", "history_date"],
    ],
}

JOB_TYPE_TABLE_VIEW = CustomTableView(
    model=JobType,
    model_name="job_type",
    fields=JOB_TYPE_MODEL_FIELDS,
    headers=JOB_TYPE_TABLE_HEADERS,
    model_relation_headers=JOB_TYPE_MODEL_RELATION_HEADERS,
    model_relation_fields=JOB_TYPE_MODEL_RELATION_FIELDS,
    search_fields_list=JOB_TYPE_SEARCH_FIELDS,
)

JOB_TYPE_VIEWS = CRUDView(
    model=JobType,
    model_name="job_type",
    model_service=JobTypeService,
    model_form=JobTypeForm,
    model_table_view=JOB_TYPE_TABLE_VIEW,
)


# ------------------------------------------------------------------------------
# Job Views
# ------------------------------------------------------------------------------

JOB_TAILWIND_CLASSES = {
    "CM": "bg-haxgreen text-[#3DAD99]",
    "NP": "bg-haxred text-[#FF4D4F]",
    "IP": "bg-haxyellow text-[#F6C000]",
    "CN": "bg-haxpurple text-[#7239EA]",
}

JOB_MODEL_FIELDS = [
    "id",
    "name",
    "description",
    "customer",
    "due_date",
    "planned_start_datetime",
    "planned_end_datetime",
    "priority",
    "job_status",
]

JOB_STATUS_FILTER_FIELD = "job_status"
JOB_SEARCH_FIELDS = ["name", "description", "customer", "id"]
JOB_TABLE_HEADERS = [
    "Job ID",
    "Job Name",
    "Description",
    "Customer",
    "Due Date",
    "Planned Start",
    "Planned End",
    "Priority",
    "Status",
]

JOB_MODEL_RELATION_HEADERS = ["TASKS", "DEPENDENCIES", "HISTORY"]

JOB_MODEL_RELATION_FIELDS = {
    # model_name: [model, related_name, [headers], [fields]]
    "tasks": [
        Task,
        "job",
        [
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
        [
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
    ],
    "dependencies": [
        "dependencies",
        ["ID", "Dependency Name", "Expected Close", "Actual Close", "Type", "Status"],
        [
            "id",
            "name",
            "expected_close_datetime",
            "actual_close_datetime",
            "dependency_type",
            "dependency_status",
        ],
    ],
    "history": [
        "history",
        [
            "ID",
            "Name",
            "User",
            "Customer",
            "Due Date",
            "Description",
            "Notes",
            "History Date",
        ],
        [
            "id",
            "name",
            "history_user",
            "customer",
            "due_date",
            "description",
            "notes",
            "history_date",
        ],
    ],
}


JobTableView = CustomTableView(
    model=Job,
    model_name="job",
    fields=JOB_MODEL_FIELDS,
    status_choices_class=JobStatusChoices,
    headers=JOB_TABLE_HEADERS,
    model_relation_headers=JOB_MODEL_RELATION_HEADERS,
    model_relation_fields=JOB_MODEL_RELATION_FIELDS,
    status_filter_field=JOB_STATUS_FILTER_FIELD,
    search_fields_list=JOB_SEARCH_FIELDS,
    tailwind_classes=JOB_TAILWIND_CLASSES,
)


JOB_VIEWS = CRUDView(
    model=Job,
    model_type=JobType,
    model_name="job",
    model_service=JobService,
    model_form=JobForm,
    model_table_view=JobTableView,
)


# ------------------------------------------------------------------------------
# TaskType Views
# ------------------------------------------------------------------------------


TASK_TYPE_MODEL_FIELDS = ["id", "external_id", "name", "notes"]
TASK_TYPE_TABLE_HEADERS = ["ID", "External ID", "Task Type Name", "Notes"]

TASK_TYPE_SEARCH_FIELDS = ["name", "notes", "external_id"]

TASK_TYPE_MODEL_RELATION_HEADERS = ["HISTORY"]
TASK_TYPE_MODEL_RELATION_FIELDS = {
    "history": [
        "history",
        ["ID", "External ID", "Name", "User", "Notes", "History Date"],
        ["id", "external_id", "name", "history_user", "notes", "history_date"],
    ],
}


TASK_TYPE_TABLE_VIEW = CustomTableView(
    model=TaskType,
    model_name="task_type",
    fields=TASK_TYPE_MODEL_FIELDS,
    headers=TASK_TYPE_TABLE_HEADERS,
    model_relation_fields=TASK_TYPE_MODEL_RELATION_FIELDS,
    model_relation_headers=TASK_TYPE_MODEL_RELATION_HEADERS,
    search_fields_list=TASK_TYPE_SEARCH_FIELDS,
)

TASK_TYPE_VIEWS = CRUDView(
    model=TaskType,
    model_name="task_type",
    model_service=TaskTypeService,
    model_form=TaskTypeForm,
    model_table_view=TASK_TYPE_TABLE_VIEW,
)


# ------------------------------------------------------------------------------
# Task Views
# ------------------------------------------------------------------------------

TASK_MODEL_FIELDS = [
    "id",
    "name",
    "job",
    "item",
    "quantity",
    "run_time_per_unit",
    "setup_time",
    "planned_start_datetime",
    "planned_end_datetime",
    "task_type",
    # TODO: Add assigned resources
    "task_status",
]

TASK_TAILWIND_CLASSES = {
    "NS": "bg-haxred text-[#FF4D4F]",
    "IP": "bg-haxyellow text-[#F6C000]",
    "CM": "bg-haxgreen text-[#3DAD99]",
}

TASK_STATUS_FILTER_FIELD = "task_status"
TASK_SEARCH_FIELDS = ["name", "item", "id"]
TASK_TABLE_HEADERS = [
    "Task ID",
    "Name",
    "Job Name",
    "Item",
    "Quantity",
    "Run Time",
    "Setup Time",
    "Planned Start",
    "Planned End",
    "Task Type",
    # TODO: Add assigned resources
    "Status",
]

TASK_MODEL_RELATION_HEADERS = ["DEPENDENCIES", "PREDECESSORS", "HISTORY", "RULES"]
TASK_MODEL_RELATION_FIELDS = {
    "dependencies": [
        "dependencies",
        ["ID", "Dependency Name", "Expected Close", "Actual Close", "Type", "Status"],
        [
            "id",
            "name",
            "expected_close_datetime",
            "actual_close_datetime",
            "dependency_type",
            "dependency_status",
        ],
    ],
    "predecessors": [
        "predecessors",
        [
            "ID",
            "Predecessor Name",
            "Item",
            "Quantity",
            "Run Time",
            "Planned Start",
            "Planned End",
            "Task Type",
            "Status",
        ],
        [
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
    ],
    "history": [
        "history",
        [
            "ID",
            "Name",
            "User",
            "Item",
            "Quantity",
            "Run Time",
            "Planned Start",
            "Planned End",
            "Task Type",
            "Status",
            "Notes",
            "History Date",
        ],
        [
            "id",
            "name",
            "history_user",
            "item",
            "quantity",
            "run_time_per_unit",
            "planned_start_datetime",
            "planned_end_datetime",
            "task_type",
            "task_status",
            "notes",
            "history_date",
        ],
    ],
    "rules": [
        TaskRuleAssignment,
        "task",
        ["ID", "Assignment Rule", "Is Applied"],
        ["id", "assigment_rule", "is_applied"],
    ],
}


TaskTableView = CustomTableView(
    model=Task,
    model_name="task",
    fields=TASK_MODEL_FIELDS,
    status_choices_class=TaskStatusChoices,
    model_relation_headers=TASK_MODEL_RELATION_HEADERS,
    model_relation_fields=TASK_MODEL_RELATION_FIELDS,
    headers=TASK_TABLE_HEADERS,
    status_filter_field=TASK_STATUS_FILTER_FIELD,
    search_fields_list=TASK_SEARCH_FIELDS,
    tailwind_classes=TASK_TAILWIND_CLASSES,
)

TASK_VIEWS = CRUDView(
    model=Task,
    model_type=TaskType,
    model_name="task",
    model_service=TaskService,
    model_form=TaskForm,
    model_table_view=TaskTableView,
)


# ------------------------------------------------------------------------------
# Dependecy Type Views
# ------------------------------------------------------------------------------

DEPENDENCY_TYPE_MODEL_FIELDS = ["id", "external_id", "name", "notes"]
DEPENDENCY_TYPE_TABLE_HEADERS = ["ID", "External ID", "Dependency Type Name", "notes"]

DEPENDENCY_TYPE_SEARCH_FIELDS = ["name", "notes", "external_id"]

DEPENDENCY_TYPE_MODEL_RELATION_HEADERS = ["HISTORY"]
DEPENDENCY_TYPE_MODEL_RELATION_FIELDS = {
    "history": [
        "history",
        ["ID", "External ID", "Name", "User", "Notes", "History Date"],
        ["id", "external_id", "name", "history_user", "notes", "history_date"],
    ],
}

DEPENDENCY_TYPE_TABLE_VIEW = CustomTableView(
    model=DependencyType,
    model_name="dependency_type",
    fields=DEPENDENCY_TYPE_MODEL_FIELDS,
    headers=DEPENDENCY_TYPE_TABLE_HEADERS,
    model_relation_headers=DEPENDENCY_TYPE_MODEL_RELATION_HEADERS,
    model_relation_fields=DEPENDENCY_TYPE_MODEL_RELATION_FIELDS,
    search_fields_list=DEPENDENCY_TYPE_SEARCH_FIELDS,
)

DEPENDENCY_TYPE_VIEWS = CRUDView(
    model=DependencyType,
    model_name="dependency_type",
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
DEPENDENCY_SEARCH_FIELDS = ["name", "id"]
DEPENDENCY_TABLE_HEADERS = [
    "Dependency ID",
    "Dependency Name",
    "Expected Close",
    "Actual Close",
    "Type",
    "Status",
]

DEPENDENCY_MODEL_RELATION_HEADERS = ["TASKS", "JOBS", "HISTORY"]

DEPENDENCY_MODEL_RELATION_FIELDS = {
    "tasks": [
        Task,
        "dependencies",
        [
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
        [
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
    ],
    "jobs": [
        Job,
        "dependencies",
        [
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
        [
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
    ],
    "history": [
        "history",
        [
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
        [
            "id",
            "name",
            "history_user",
            "expected_close_datetime",
            "actual_close_datetime",
            "dependency_type",
            "dependency_status",
            "notes",
            "history_date",
        ],
    ],
}

DependencyTableView = CustomTableView(
    model=Dependency,
    model_name="dependency",
    fields=DEPENDENCY_MODEL_FIELDS,
    status_choices_class=DependencyStatusChoices,
    model_relation_fields=DEPENDENCY_MODEL_RELATION_FIELDS,
    model_relation_headers=DEPENDENCY_MODEL_RELATION_HEADERS,
    headers=DEPENDENCY_TABLE_HEADERS,
    status_filter_field=DEPENDENCY_STATUS_FILTER_FIELD,
    search_fields_list=DEPENDENCY_SEARCH_FIELDS,
    tailwind_classes=DEPENDENCY_TAILWIND_CLASSES,
)

DEPENDENCY_VIEWS = CRUDView(
    model=Dependency,
    model_type=DependencyType,
    model_name="dependency",
    model_service=DependencyService,
    model_form=DependencyForm,
    model_table_view=DependencyTableView,
)

# ------------------------------------------------------------------------------
# Item Views
# ------------------------------------------------------------------------------

ITEM_MODEL_FIELDS = ["id", "external_id", "name", "description", "notes"]
ITEM_TABLE_HEADERS = ["ID", "External ID", "Item Name", "Description", "Notes"]

ITEM_SEARCH_FIELDS = ["name", "description", "notes", "external_id"]

ITEM_MODEL_RELATION_HEADERS = ["HISTORY"]
ITEM_MODEL_RELATION_FIELDS = {
    "history": [
        "history",
        ["ID", "External ID", "Name", "User", "Notes", "History Date"],
        ["id", "external_id", "name", "history_user", "notes", "history_date"],
    ],
}

ITEM_TABLE_VIEW = CustomTableView(
    model=Item,
    model_name="item",
    fields=ITEM_MODEL_FIELDS,
    headers=ITEM_TABLE_HEADERS,
    model_relation_headers=ITEM_MODEL_RELATION_HEADERS,
    model_relation_fields=ITEM_MODEL_RELATION_FIELDS,
    search_fields_list=ITEM_SEARCH_FIELDS,
)

ITEM_VIEWS = CRUDView(
    model=Item,
    model_name="item",
    model_service=ItemService,
    model_form=ItemForm,
    model_table_view=ITEM_TABLE_VIEW,
)
