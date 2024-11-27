from common.views import CRUDView, CustomTableView

# Create your views here.
from resource_assigner.forms import AssignmentConstraintForm
from common.models import Operator
from resource_assigner.models import AssignmentConstraint
from resource_assigner.services import AssignmentConstraintService


# ------------------------------------------------------------------------------
# AssignmentConstraint Views
# ------------------------------------------------------------------------------

ASSIGNMENT_CONSTRAINT_MODEL_FIELDS = [
    "id",
    "task",
    "assignment_rule",
    "resource_group",
    "resources",
    "resource_count",
    "use_all_resources",
]

ASSIGNMENT_CONSTRAINT_SEARCH_FIELDS = [
    "task",
    "assignment_rule",
    "resource_group",
    "resources",
    "resource_count",
    "use_all_resources",
]

ASSIGNMENT_CONSTRAINT_MODEL_RELATION_HEADERS = [
    "Resources",
    "History",
]

ASSIGNMENT_CONSTRAINT_MODEL_RELATION_FIELDS = {
    "resources": {
        "model_name": "resources",
        "related_name": "resources",
        "headers": ["ID", "Resource Name"],
        "fields": ["id", "name"],
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


ASSIGNMENT_CONSTRAINT_TABLE_VIEW = CustomTableView(
    model=AssignmentConstraint,
    model_name="assignment_constraint",
    fields=ASSIGNMENT_CONSTRAINT_MODEL_FIELDS,
    search_fields_list=ASSIGNMENT_CONSTRAINT_SEARCH_FIELDS,
    model_relation_headers=ASSIGNMENT_CONSTRAINT_MODEL_RELATION_HEADERS,
    model_relation_fields=ASSIGNMENT_CONSTRAINT_MODEL_RELATION_FIELDS,
)

ASSIGNMENT_CONSTRAINT_VIEWS = CRUDView(
    model=AssignmentConstraint,
    model_name="assignment_constraints",
    model_service=AssignmentConstraintService,
    model_form=AssignmentConstraintForm,
    model_table_view=ASSIGNMENT_CONSTRAINT_TABLE_VIEW,
)