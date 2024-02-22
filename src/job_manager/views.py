# views.py

from common.views import CRUDView, CustomTableView

from .forms import JobForm, TaskForm, DependencyForm
from .models import Job, JobType, JobStatusChoices, Task, TaskType, TaskStatusChoices, Dependency, DependencyType, DependencyStatusChoices
from .services import JobService, TaskService, DependencyService

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

JOB_MODEL_RELATION_HEADERS = ["TASKS", "DEPENDENCIES"]

JOB_MODEL_RELATION_FIELDS = {
    # model_name: [model, related_name, [headers], [fields]]
    "tasks": [Task, "job", ["Task Name", "Item", "Quantity", "Run Time", "Planned Start", "Planned End", "Task Type", "Status"], ["name", "item", "quantity", "run_time_per_unit", "planned_start_datetime", "planned_end_datetime", "task_type", "task_status"]],
    "dependencies": ["dependencies", ["Dependency Name", "Expected Close", "Actual Close", "Type", "Status"], ["name", "expected_close_datetime", "actual_close_datetime", "dependency_type", "dependency_status"]],
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
# Task Views
# ------------------------------------------------------------------------------

TASK_MODEL_FIELDS = [
    "id",
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

TASK_MODEL_RELATION_HEADERS = ["DEPENDENCIES", "Assignment Rules"]
TASK_MODEL_RELATION_FIELDS = {

    "dependencies": ["dependencies", ["Dependency Name", "Expected Close", "Actual Close", "Type", "Status"], ["name", "expected_close_datetime", "actual_close_datetime", "dependency_type", "dependency_status"]],
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

DEPENDENCY_MODEL_RELATION_HEADERS = ["TASKS", "JOBS"]

DEPENDENCY_MODEL_RELATION_FIELDS = {
    "tasks": [Task, "dependencies", ["Task Name", "Item", "Quantity", "Run Time", "Planned Start", "Planned End", "Task Type", "Status"], ["name", "item", "quantity", "run_time_per_unit", "planned_start_datetime", "planned_end_datetime", "task_type", "task_status"]],
    "jobs": [Job, "dependencies", ["Job Name", "Description", "Customer", "Due Date", "Planned Start", "Planned End", "Priority", "Status"], ["name", "description", "customer", "due_date", "planned_start_datetime", "planned_end_datetime", "priority", "job_status"]],
}

DependencyTableView = CustomTableView(
    model=Dependency,
    model_name="dependency",
    fields=DEPENDENCY_MODEL_FIELDS,
    status_choices_class=DependencyStatusChoices,
    model_relation_fields=DEPENDENCY_MODEL_FIELDS,
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

