from common.utils.views import get_model_fields
from common.views import CRUDView, CustomTableView

# Create your views here.
from resource_assigner.forms import (
    AssigmentRuleCriteriaForm,
    AssigmentRuleForm,
    AssignmentConstraintForm,
)
from common.models import Operator
from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    AssignmentConstraint,
    TaskRuleAssignment,
)
from resource_assigner.services import (
    AssigmentRuleCriteriaService,
    AssigmentRuleService,
)


# ------------------------------------------------------------------------------
# AssigmentRule Views
# ------------------------------------------------------------------------------

ASSIGMENT_RULE_MODEL_FIELDS = [
    "id",
    "order",
    "name",
    "notes",
    "description",
    "work_center",
    "is_active",
]

ASSIGMENT_RULE_SEARCH_FIELDS = ["name", "description", "id", "notes", "work_center"]

ASSIGMENT_RULE_MODEL_RELATION_HEADERS = [
    "RULE CRITERIA",
    "TASK",
    "HISTORY",
]

ASSIGMENT_RULE_MODEL_RELATION_FIELDS = {
    "rule_criteria": {
        "model": AssigmentRuleCriteria,
        "model_name": "assigment_rule_criteria",
        "related_name": "assigment_rule",
        "headers": ["ID", "field", "operator", "value"],
        "fields": ["id", "field", "operator", "value"],
        "show_edit_actions": False,
    },
    "task": {
        "model": TaskRuleAssignment,
        "model_name": "task_rule_assignment",
        "related_name": "assigment_rule",
        "headers": ["ID", "Task", "Rule Applied"],
        "fields": ["id", "task", "is_applied"],
        "show_edit_actions": False,
    },
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "History Date", "History Type", "History User"],
        "fields": ["history_id", "history_date", "history_type", "history_user"],
        "show_edit_actions": False,
    },
}


# AssigmentRule Formset Options
ASSIGMENT_RULE_CRITERIA_FORMSET_FORM_FIELDS = ["field", "operator", "value"]

ASSIGMENT_RULE_CRITERIA_FORMSET_OPTIONS = [
    AssigmentRuleCriteria,
    AssigmentRuleCriteriaForm,
    "criteria",
    ASSIGMENT_RULE_CRITERIA_FORMSET_FORM_FIELDS,
    "assigment_rule_criteria",
]

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
    "assignment_constraints",
    ASSIGMENT_CONSTRAINT_FORMSET_FORM_FIELDS,
    "assignment_constraint",
]

ASSIGMENT_RULE_TABLE_VIEW = CustomTableView(
    model=AssigmentRule,
    model_name="assigment_rule",
    fields=ASSIGMENT_RULE_MODEL_FIELDS,
    model_relation_headers=ASSIGMENT_RULE_MODEL_RELATION_HEADERS,
    model_relation_fields=ASSIGMENT_RULE_MODEL_RELATION_FIELDS,
    search_fields_list=ASSIGMENT_RULE_SEARCH_FIELDS,
    order_by_field="order",
)

ASSIGMENT_RULE_VIEWS = CRUDView(
    model=AssigmentRule,
    model_name="assigment_rules",
    model_service=AssigmentRuleService,
    model_form=AssigmentRuleForm,
    model_table_view=ASSIGMENT_RULE_TABLE_VIEW,
    ordered_model=True,
    formset_options=ASSIGMENT_RULE_CRITERIA_FORMSET_OPTIONS,
    inline_formset=ASSIGMENT_RULE_CONSTRAINT_FORMSET_OPTIONS,
    list_template_name="resource_assigner/assignment_rule/list.html",
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

ASSIGMENT_RULE_CRITERIA_SEARCH_FIELDS = ["assigment_rule", "field", "operator", "value"]

ASSIGNMENT_STATUS_FILTER_FIELD = "operator"

ASSIGMENT_RULE_CRITERIA_TABLE_VIEW = CustomTableView(
    model=AssigmentRuleCriteria,
    model_name="assigment_rule_criteria",
    fields=ASSIGMENT_RULE_CRITERIA_MODEL_FIELDS,
    search_fields_list=ASSIGMENT_RULE_CRITERIA_SEARCH_FIELDS,
    status_filter_field=ASSIGNMENT_STATUS_FILTER_FIELD,
)

ASSIGMENT_RULE_CRITERIA_VIEWS = CRUDView(
    model=AssigmentRuleCriteria,
    model_name="assigment_rule_criteria",
    model_service=AssigmentRuleCriteriaService,
    model_form=AssigmentRuleCriteriaForm,
    model_table_view=ASSIGMENT_RULE_CRITERIA_TABLE_VIEW,
    sub_model_relation=True,
)
