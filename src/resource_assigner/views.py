from common.views import CRUDView, CustomTableView
# Create your views here.

from .forms import *
from .models import *
from .services import *


# ------------------------------------------------------------------------------
# Task Resource Assignement Views
# ------------------------------------------------------------------------------

TASK_RESOURCE_ASSIGNMENT_MODEL_FIELDS = [
    "id",
    "task",
    "assigment_rule",
    "resource_count",
    "use_all_resources",
]

TASK_RESOURCE_ASSIGNMENT_TABLE_HEADERS = [
    "ID",
    "Task",
    "Assigment Rule",
    "Resource Count",
    "Use All Resources",
]

TASK_RESOURCE_ASSIGNMENT_SEARCH_FIELDS = ["task", "assigment_rule"]

TASK_RESOURCE_ASSIGNMENT_RELATION_HEADERS = [
    "Resource Pool",
]

TASK_RESOURCE_ASSIGNMENT_RELATION_FIELDS = {
    "resource_pool": ["resource_pool", ["ID", "Resource Pool Name"], ["id", "name"]],
}

TASK_RESOURCE_ASSIGNMENT_TABLE_VIEW = CustomTableView(
    model=TaskResourceAssigment,
    model_name="task_resource_assigment",
    fields=TASK_RESOURCE_ASSIGNMENT_MODEL_FIELDS,
    headers=TASK_RESOURCE_ASSIGNMENT_TABLE_HEADERS,
    search_fields_list=TASK_RESOURCE_ASSIGNMENT_SEARCH_FIELDS,
    model_relation_headers=TASK_RESOURCE_ASSIGNMENT_RELATION_HEADERS,
    model_relation_fields=TASK_RESOURCE_ASSIGNMENT_RELATION_FIELDS,
)

TASK_RESOURCE_ASSIGNMENT_VIEWS = CRUDView(
    model=TaskResourceAssigment,
    model_name="task_resource_assigment",
    model_service=TaskResourceAssigmentService,
    model_form=TaskResourceAssigmentForm,
    model_table_view=TASK_RESOURCE_ASSIGNMENT_TABLE_VIEW,
)

# ------------------------------------------------------------------------------
# AssigmentRule Views
# ------------------------------------------------------------------------------

ASSIGMENT_RULE_MODEL_FIELDS = [
    "id",
    "external_id",
    "notes",
    "name",
    "description",
    "work_center",
    "is_active",
]
ASSIGMENT_RULE_TABLE_HEADERS = [
    "ID",
    "External ID",
    "Notes",
    "Name",
    "Description",
    "Work Center",
    "Is Active",
]

ASSIGMENT_RULE_SEARCH_FIELDS = ["name", "description", "external_id"]

ASSIGMENT_RULE_TABLE_VIEW = CustomTableView(
    model=AssigmentRule,
    model_name="assigment_rule",
    fields=ASSIGMENT_RULE_MODEL_FIELDS,
    headers=ASSIGMENT_RULE_TABLE_HEADERS,
    search_fields_list=ASSIGMENT_RULE_SEARCH_FIELDS,
)

ASSIGMENT_RULE_VIEWS = CRUDView(
    model=AssigmentRule,
    model_name="assigment_rule",
    model_service=AssigmentRuleService,
    model_form=AssigmentRuleForm,
    model_table_view=ASSIGMENT_RULE_TABLE_VIEW,
)


# ------------------------------------------------------------------------------
# AssigmentRuleCriteria Views
# ------------------------------------------------------------------------------

ASSIGMENT_RULE_CRITERIA_MODEL_FIELDS = [
    "id",
    "assigment_rule",
    "field",
    "operator",
    "value",
]
ASSIGMENT_RULE_CRITERIA_TABLE_HEADERS = [
    "ID",
    "Assigment Rule",
    "Field",
    "Operator",
    "Value",
]

ASSIGMENT_RULE_CRITERIA_SEARCH_FIELDS = ["assigment_rule", "field", "operator", "value"]

ASSIGNMENT_STATUS_FILTER_FIELD = "operator"

ASSIGMENT_RULE_CRITERIA_TABLE_VIEW = CustomTableView(
    model=AssigmentRuleCriteria,
    model_name="assigment_rule_criteria",
    fields=ASSIGMENT_RULE_CRITERIA_MODEL_FIELDS,
    headers=ASSIGMENT_RULE_CRITERIA_TABLE_HEADERS,
    search_fields_list=ASSIGMENT_RULE_CRITERIA_SEARCH_FIELDS,
    status_filter_field=ASSIGNMENT_STATUS_FILTER_FIELD,
)

ASSIGMENT_RULE_CRITERIA_VIEWS = CRUDView(
    model=AssigmentRuleCriteria,
    model_name="assigment_rule_criteria",
    model_service=AssigmentRuleCriteriaService,
    model_form=AssigmentRuleCriteriaForm,
    model_table_view=ASSIGMENT_RULE_CRITERIA_TABLE_VIEW,
)


# ------------------------------------------------------------------------------
# AssignmentConstraint Views
# ------------------------------------------------------------------------------

ASSIGNMENT_CONSTRAINT_MODEL_FIELDS = [
    "id",
    "task",
    "assignment_rule",
    "resource_pool",
    "resources",
    "work_units",
    "required_units",
    "is_active",
    "is_direct",
]

ASSIGNMENT_CONSTRAINT_TABLE_HEADERS = [
    "ID",
    "Task",
    "Assignment Rule",
    "Resource Pool",
    "Resources",
    "Work Units",
    "Required Units",
    "Is Active",
    "Is Direct",
]

ASSIGNMENT_CONSTRAINT_SEARCH_FIELDS = [
    "task",
    "assignment_rule",
    "resource_pool",
    "resources",
    "work_units",
    "required_units",
    "is_active",
    "is_direct",
]

ASSIGNMENT_CONSTRAINT_RELATION_HEADERS = [
    "Resources",
    "Work_Units",
]

ASSIGNMENT_CONSTRAINT_RELATION_FIELDS = {
    "resources": ["resources", ["ID", "Resource Name"], ["id", "name"]],
    "work_units": ["work_units", ["ID", "Work Unit Name"], ["id", "name"]],
}


ASSIGNMENT_CONSTRAINT_TABLE_VIEW = CustomTableView(
    model=AssignmentConstraint,
    model_name="assignment_constraint",
    fields=ASSIGNMENT_CONSTRAINT_MODEL_FIELDS,
    headers=ASSIGNMENT_CONSTRAINT_TABLE_HEADERS,
    search_fields_list=ASSIGNMENT_CONSTRAINT_SEARCH_FIELDS,
    model_relation_headers=ASSIGNMENT_CONSTRAINT_RELATION_HEADERS,
    model_relation_fields=ASSIGNMENT_CONSTRAINT_RELATION_FIELDS,
)

ASSIGNMENT_CONSTRAINT_VIEWS = CRUDView(
    model=AssignmentConstraint,
    model_name="assignment_constraint",
    model_service=AssignmentConstraintService,
    model_form=AssignmentConstraintForm,
    model_table_view=ASSIGNMENT_CONSTRAINT_TABLE_VIEW,
)
