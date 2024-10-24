# views.py
from django.conf import settings
from common.views import CRUDView, CustomTableView
from django.shortcuts import redirect, render
from django.urls import reverse
from resource_assigner.models import AssignmentConstraint, TaskRuleAssignment

from .forms import (
    DependencyForm,
    DependencyTypeForm,
    ItemForm,
    JobForm,
    JobTypeForm,
    TaskForm,
    TaskTypeForm,
    WorkCenterForm,
    AssignmentConstraintForm,
)
from .models import (
    Dependency,
    DependencyStatusChoices,
    DependencyType,
    Item,
    Job,
    JobStatusChoices,
    JobType,
    Task,
    TaskStatusChoices,
    TaskType,
    WorkCenter,
)
from .services import (
    DependencyService,
    DependencyTypeService,
    ItemService,
    JobService,
    JobTypeService,
    TaskService,
    TaskTypeService,
    WorkCenterService,
)

from resource_assigner.models import AssignmentConstraint

# ------------------------------------------------------------------------------
# WorkCenter Views
# ------------------------------------------------------------------------------

WORK_CENTER_MODEL_FIELDS = ["id", "name", "notes"]
WORK_CENTER_SEARCH_FIELDS = ["name", "id"]

WORK_CENTER_MODEL_RELATION_HEADERS = ["HISTORY"]
WORK_CENTER_FIELD_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "Name", "User", "Notes", "History Date"],
        "fields": ["history_id", "name", "history_user", "notes", "history_date"],
        "show_edit_actions": False,
    },
}

WorkCenterTableView = CustomTableView(
    model=WorkCenter,
    model_name="work_center",
    fields=WORK_CENTER_MODEL_FIELDS,
    model_relation_headers=WORK_CENTER_MODEL_RELATION_HEADERS,
    model_relation_fields=WORK_CENTER_FIELD_MODEL_RELATION_FIELDS,
    search_fields_list=WORK_CENTER_SEARCH_FIELDS,
)

WORK_CENTER_VIEWS = CRUDView(
    model=WorkCenter,
    model_name="work_centers",
    model_service=WorkCenterService,
    model_form=WorkCenterForm,
    model_table_view=WorkCenterTableView,
)


# ------------------------------------------------------------------------------
# Job Type Views
# ------------------------------------------------------------------------------

JOB_TYPE_MODEL_FIELDS = ["id", "name", "notes"]

JOB_TYPE_SEARCH_FIELDS = ["name", "notes", "external_id"]

JOB_TYPE_MODEL_RELATION_HEADERS = ["HISTORY"]
JOB_TYPE_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "Name", "User", "Notes", "History Date"],
        "fields": ["history_id", "name", "history_user", "notes", "history_date"],
        "show_edit_actions": False,
    },
}

JOB_TYPE_TABLE_VIEW = CustomTableView(
    model=JobType,
    model_name="job_type",
    fields=JOB_TYPE_MODEL_FIELDS,
    model_relation_headers=JOB_TYPE_MODEL_RELATION_HEADERS,
    model_relation_fields=JOB_TYPE_MODEL_RELATION_FIELDS,
    search_fields_list=JOB_TYPE_SEARCH_FIELDS,
)

JOB_TYPE_VIEWS = CRUDView(
    model=JobType,
    model_name="job_types",
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

JOB_MODEL_RELATION_HEADERS = ["TASKS", "DEPENDENCIES", "HISTORY"]

JOB_MODEL_RELATION_FIELDS = {
    # model_name: [model, related_name, [headers], [fields]]
    "tasks": {
        "model": Task,
        "model_name": "task",
        "related_name": "job",
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
    "dependencies": {
        "model_name": "dependency",
        "related_name": "dependencies",
        "headers": [
            "ID",
            "Dependency Name",
            "Expected Close",
            "Actual Close",
            "Type",
            "Status",
        ],
        "fields": [
            "id",
            "name",
            "expected_close_datetime",
            "actual_close_datetime",
            "dependency_type",
            "dependency_status",
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
            "Customer",
            "Due Date",
            "Description",
            "Notes",
            "History Date",
        ],
        "fields": [
            "history_id",
            "name",
            "history_user",
            "customer",
            "due_date",
            "description",
            "notes",
            "history_date",
        ],
        "show_edit_actions": False,
    },
}


JobTableView = CustomTableView(
    model=Job,
    model_name="job",
    fields=JOB_MODEL_FIELDS,
    status_choices_class=JobStatusChoices,
    model_relation_headers=JOB_MODEL_RELATION_HEADERS,
    model_relation_fields=JOB_MODEL_RELATION_FIELDS,
    status_filter_field=JOB_STATUS_FILTER_FIELD,
    search_fields_list=JOB_SEARCH_FIELDS,
    tailwind_classes=JOB_TAILWIND_CLASSES,
)


JOB_VIEWS = CRUDView(
    model=Job,
    model_type=JobType,
    model_name="jobs",
    model_service=JobService,
    model_form=JobForm,
    model_table_view=JobTableView,
)


# ------------------------------------------------------------------------------
# TaskType Views
# ------------------------------------------------------------------------------


TASK_TYPE_MODEL_FIELDS = ["id", "name", "notes"]

TASK_TYPE_SEARCH_FIELDS = ["name", "notes", "external_id"]

TASK_TYPE_MODEL_RELATION_HEADERS = ["HISTORY"]
TASK_TYPE_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "Name", "User", "Notes", "History Date"],
        "fields": ["history_id", "name", "history_user", "notes", "history_date"],
        "show_edit_actions": False,
    },
}


TASK_TYPE_TABLE_VIEW = CustomTableView(
    model=TaskType,
    model_name="task_type",
    fields=TASK_TYPE_MODEL_FIELDS,
    model_relation_fields=TASK_TYPE_MODEL_RELATION_FIELDS,
    model_relation_headers=TASK_TYPE_MODEL_RELATION_HEADERS,
    search_fields_list=TASK_TYPE_SEARCH_FIELDS,
)

TASK_TYPE_VIEWS = CRUDView(
    model=TaskType,
    model_name="task_types",
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

TASK_MODEL_RELATION_HEADERS = [
    "DEPENDENCIES",
    "PREDECESSORS",
    "HISTORY",
    "CONSTRAINTS",
    "RULES",
]
TASK_MODEL_RELATION_FIELDS = {
    "dependencies": {
        "model_name": "tasks",
        "related_name": "dependencies",
        "headers": [
            "ID",
            "Dependency Name",
            "Expected Close",
            "Actual Close",
            "Type",
            "Status",
        ],
        "fields": [
            "id",
            "name",
            "expected_close_datetime",
            "actual_close_datetime",
            "dependency_type",
            "dependency_status",
        ],
        "show_edit_actions": False,
    },
    "predecessors": {
        "model_name": "tasks",
        "related_name": "predecessors",
        "headers": [
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
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": [
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
        "fields": [
            "history_id",
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
        "show_edit_actions": False,
    },
    "rules": {
        "model": TaskRuleAssignment,
        "model_name": "task_rule_assignments",
        "related_name": "task",
        "model_name": "task_rule_assignment",
        "headers": ["ID", "Assignment Rule", "Is Applied"],
        "fields": ["id", "assigment_rule", "is_applied"],
        "show_edit_actions": False,
    },
    "constraints": {
        "model": AssignmentConstraint,
        "model_name": "constraint",
        "related_name": "task",
        "headers": [
            "ID",
            "Assignment Rule",
            "Resource Group",
            "Resource Count",
            "Use All Resources",
        ],
        "fields": [
            "id",
            "assignment_rule",
            "resource_group",
            "resource_count",
            "use_all_resources",
        ],
        "show_edit_actions": False,
    },
}

# AssigmentConstraint Formset Options
ASSIGMENT_CONSTRAINT_FORMSET_FORM_FIELDS = [
    "resource_group",
    "resources",
    "resource_count",
    "use_all_resources",
]

ASSIGMENT_RULE_CONSTRAINT_FORMSET_OPTIONS = [
    AssignmentConstraint,
    AssignmentConstraintForm,
    "constraints",
    ASSIGMENT_CONSTRAINT_FORMSET_FORM_FIELDS,
    "assignment_constraint",
]

TaskTableView = CustomTableView(
    model=Task,
    model_name="task",
    fields=TASK_MODEL_FIELDS,
    status_choices_class=TaskStatusChoices,
    model_relation_headers=TASK_MODEL_RELATION_HEADERS,
    model_relation_fields=TASK_MODEL_RELATION_FIELDS,
    status_filter_field=TASK_STATUS_FILTER_FIELD,
    search_fields_list=TASK_SEARCH_FIELDS,
    tailwind_classes=TASK_TAILWIND_CLASSES,
)

TASK_VIEWS = CRUDView(
    model=Task,
    model_type=TaskType,
    model_name="tasks",
    model_service=TaskService,
    model_form=TaskForm,
    inline_formset=ASSIGMENT_RULE_CONSTRAINT_FORMSET_OPTIONS,
    model_table_view=TaskTableView,
)


# ------------------------------------------------------------------------------
# Dependecy Type Views
# ------------------------------------------------------------------------------

DEPENDENCY_TYPE_MODEL_FIELDS = ["id", "name", "notes"]

DEPENDENCY_TYPE_SEARCH_FIELDS = ["name", "notes", "external_id"]

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
DEPENDENCY_SEARCH_FIELDS = ["name", "id"]

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

DependencyTableView = CustomTableView(
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
    model_table_view=DependencyTableView,
)

# ------------------------------------------------------------------------------
# Item Views
# ------------------------------------------------------------------------------

ITEM_MODEL_FIELDS = ["id", "name", "description", "notes"]

ITEM_SEARCH_FIELDS = ["name", "description", "notes", "external_id"]

ITEM_MODEL_RELATION_HEADERS = ["HISTORY"]
ITEM_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "Name", "User", "Notes", "History Date"],
        "fields": ["history_id", "name", "history_user", "notes", "history_date"],
        "show_edit_actions": False,
    },
}

ITEM_TABLE_VIEW = CustomTableView(
    model=Item,
    model_name="item",
    fields=ITEM_MODEL_FIELDS,
    model_relation_headers=ITEM_MODEL_RELATION_HEADERS,
    model_relation_fields=ITEM_MODEL_RELATION_FIELDS,
    search_fields_list=ITEM_SEARCH_FIELDS,
)

ITEM_VIEWS = CRUDView(
    model=Item,
    model_name="items",
    model_service=ItemService,
    model_form=ItemForm,
    model_table_view=ITEM_TABLE_VIEW,
)

# ------------------------------------------------------------------------------
# JOB-TASK gantt-chart View
# ------------------------------------------------------------------------------


def dashboard_gantt_chart_view(request, gantt_type: str = "job", home: str = "true"):
    """
    Dashboard
        Job Task gantt chart data view

    Args:
        request (HttpRequest): The HTTP request object.
        gantt_type (str): The type of Gantt chart to display. Defaults to "job".

    Returns:
        HttpResponse: The HTTP response with the rendered Gantt chart view.
    """
    if request.user.require_password_change:
        return redirect(reverse("users:change_password"))

    if "HX-Request" in request.headers and home == "false":
        if gantt_type == "job":
            return render(
                request,
                "dashboard/job_task_gantt.html",
                {
                    "gantt_chart_title": "Job Task",
                    "API_BASE_URL": settings.API_BASE_URL,
                },
            )
        else:
            return render(
                request,
                "dashboard/resource_gantt.html",
                {
                    "gantt_chart_title": "Resource",
                    "API_BASE_URL": settings.API_BASE_URL,
                },
            )

    return render(
        request,
        "dashboard/base.html",
        {
            "gantt_chart_title": "Job Task",
            "gantt_chart": "dashboard/job_task_gantt.html",
            "API_BASE_URL": settings.API_BASE_URL,
        },
    )
