from common.views import CRUDView, CustomTableView

# Create your views here.
from resource_assigner.forms import TaskResourceAssigmentForm
from resource_assigner.models import TaskResourceAssigment
from resource_assigner.services import TaskResourceAssigmentService


# ------------------------------------------------------------------------------
# Task Resource Assignement Views
# ------------------------------------------------------------------------------

TASK_RESOURCE_ASSIGNMENT_MODEL_FIELDS = [
    "id",
    "task",
]

TASK_RESOURCE_ASSIGNMENT_SEARCH_FIELDS = ["id", "task", "assigment_rule"]

TASK_RESOURCE_ASSIGNMENT_TABLE_VIEW = CustomTableView(
    model=TaskResourceAssigment,
    model_name="task_resource_assigment",
    fields=TASK_RESOURCE_ASSIGNMENT_MODEL_FIELDS,
    search_fields_list=TASK_RESOURCE_ASSIGNMENT_SEARCH_FIELDS,
)

TASK_RESOURCE_ASSIGNMENT_VIEWS = CRUDView(
    model=TaskResourceAssigment,
    model_name="task_resource_assigments",
    model_service=TaskResourceAssigmentService,
    model_form=TaskResourceAssigmentForm,
    model_table_view=TASK_RESOURCE_ASSIGNMENT_TABLE_VIEW,
)
