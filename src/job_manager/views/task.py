# views.py
from common.views import CRUDView, CustomTableView
from resource_assigner.models import AssignmentConstraint, TaskRuleAssignment

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
)
