# views.py
from datetime import date, datetime
from django.shortcuts import render

from common.views import CRUDView, CustomTableView
from resource_assigner.models import AssignmentConstraint, TaskRuleAssignment
from common.utils.views import convert_timestamp, convert_date

from job_manager.forms import (
    AssignmentConstraintForm,
    TaskForm,
    TaskTypeForm,
    WorkCenterForm,
)
from job_manager.models import (
    Task,
    TaskStatusChoices,
    TaskType,
    WorkCenter,
)
from job_manager.services import (
    TaskService,
    TaskTypeService,
    WorkCenterService,
)


# ------------------------------------------------------------------------------
# WorkCenter Views
# ------------------------------------------------------------------------------

WORK_CENTER_MODEL_FIELDS = ["id", "name", "notes"]
WORK_CENTER_SEARCH_FIELDS = ["name", "id", "notes"]

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

WORK_CENTER_TABLE_VIEW = CustomTableView(
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
    model_table_view=WORK_CENTER_TABLE_VIEW,
)


# ------------------------------------------------------------------------------
# TaskType Views
# ------------------------------------------------------------------------------


TASK_TYPE_MODEL_FIELDS = ["id", "name", "notes"]

TASK_TYPE_SEARCH_FIELDS = ["name", "notes", "id"]

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
    "task_status",
]

TASK_TAILWIND_CLASSES = {
    "NS": "bg-haxred text-[#FF4D4F]",
    "IP": "bg-haxyellow text-[#F6C000]",
    "CM": "bg-haxgreen text-[#3DAD99]",
}

TASK_STATUS_FILTER_FIELD = "task_status"
TASK_SEARCH_FIELDS = ["id", "name", "item", "job", "task_type", "work_center", "notes"]

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

TASK_TABLE_VIEW = CustomTableView(
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
    model_table_view=TASK_TABLE_VIEW,
    list_template_name="job_manager/task/list.html",
)


# ------------------------------------------------------------------------------
# Task Parent Child Views
# ------------------------------------------------------------------------------


def get_sub_tasks(request, id, number_of_rows=25):
    """
    Retrieve and process sub-tasks for a given task.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the parent task.
        number_of_rows (int, optional): The maximum number of sub-tasks to retrieve. Defaults to 25.

    Returns:
        HttpResponse: The rendered HTML response containing the sub-tasks data.

    The function performs the following steps:
    1. Retrieves the parent task instance using the provided ID.
    2. Filters and retrieves sub-tasks associated with the parent task.
    3. Processes each sub-task to extract and format relevant field data.
    4. Constructs a context dictionary containing the processed sub-tasks and headers.
    5. Renders and returns an HTML response if the request contains the "HX-Request" header.

    Field processing includes:
    - Incrementing the "order" field by 1.
    - Formatting the "status" field with appropriate CSS classes and display values.
    - Converting datetime and date fields to a specific format.
    - Directly appending other field values.

    The rendered HTML response is based on the "job_manager/task/child_task.html" template.
    """
    task_instance = Task.objects.get(id=id)

    data = Task.objects.filter(parent=task_instance)

    rows = []
    for instance in data[:number_of_rows]:
        row_data = []
        for field in TASK_MODEL_FIELDS:
            if field == "order":
                # Get order field value and increment it by 1
                value = getattr(instance, field) + 1
                row_data.append(value)
            elif "status" in field:
                value = (
                    f'<span class="{TASK_TAILWIND_CLASSES.get(getattr(instance, field))} text-xs font-medium px-2 py-0.5 rounded whitespace-nowrap">'
                    f'{getattr(instance, "get_task_status_display")() if hasattr(instance, "get_task_status_display") else TASK_TAILWIND_CLASSES.get(getattr(instance, field))}</span>',
                )
                row_data.append(value[0])
            elif isinstance(getattr(instance, field), datetime):
                value = convert_timestamp(getattr(instance, field))
                row_data.append(value)
            elif isinstance(getattr(instance, field), date):
                value = convert_date(getattr(instance, field))
                row_data.append(value)
            else:
                value = getattr(instance, field)
                row_data.append(value)

        rows.append(row_data)

    context = {
        "rows": rows,
        "current_id": id,
        "headers": TASK_MODEL_FIELDS,
    }

    if "HX-Request" in request.headers:
        return render(
            request,
            "job_manager/task/child_task.html",
            context,
        )
