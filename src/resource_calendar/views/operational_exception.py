from common.views import CRUDView, CustomTableView

# Create your views here.
from resource_calendar.models import (
    OperationalException,
    OperationalExceptionType,
)
from resource_calendar.forms import OperationalExceptionForm, OperationalExceptionTypeForm
from resource_calendar.services import OperationalExceptionService, OperationalExceptionTypeService


# ------------------------------------------------------------------------------
# Operational Exception Type VIEWS
# ------------------------------------------------------------------------------

OPERATIONAL_EXCEPTION_TYPE_MODEL_FIELDS = ["id", "name", "notes"]
OPERATIONAL_EXCEPTION_TYPE_SEARCH_FIELDS = ["name", "id"]

OPERATIONAL_EXCEPTION_TYPE_MODEL_RELATION_HEADERS = ["HISTORY"]
OPERATIONAL_EXCEPTION_TYPE_MODEL_RELATION_FIELDS = {
    "history": {
        "related_name": "history",
        "model_name": "history",
        "headers": ["ID", "History Date", "History Type", "History User"],
        "fields": ["history_id", "history_date", "history_type", "history_user"],
        "show_edit_actions": False,
    },
}

OPERATIONAL_EXCEPTION_TYPE_TABLE_VIEWS = CustomTableView(
    model=OperationalExceptionType,
    model_name="operational_exception_type",
    fields=OPERATIONAL_EXCEPTION_TYPE_MODEL_FIELDS,
    model_relation_headers=OPERATIONAL_EXCEPTION_TYPE_MODEL_RELATION_HEADERS,
    model_relation_fields=OPERATIONAL_EXCEPTION_TYPE_MODEL_RELATION_FIELDS,
    search_fields_list=OPERATIONAL_EXCEPTION_TYPE_SEARCH_FIELDS,
)

OPERATIONAL_EXCEPTION_TYPE_VIEWS = CRUDView(
    model=OperationalExceptionType,
    model_name="operational_exception_types",
    model_service=OperationalExceptionTypeService,
    model_form=OperationalExceptionTypeForm,
    model_table_view=OPERATIONAL_EXCEPTION_TYPE_TABLE_VIEWS,
)


# ------------------------------------------------------------------------------
# Operational Exception VIEWS
# ------------------------------------------------------------------------------

OPERATIONAL_EXCEPTION_MODEL_FIELDS = [
    "id",
    "resource",
    "operational_exception_type",
    "weekly_shift_template",
    "start_datetime",
    "end_datetime",
    "notes",
]

OPERATIONAL_EXCEPTION_SEARCH_FIELDS = [
    "id",
    "operational_exception_type",
    "weekly_shift_template",
    "resource",
    "notes",
]

OPERATIONAL_EXCEPTION_MODEL_RELATION_HEADERS = ["HISTORY"]
OPERATIONAL_EXCEPTION_MODEL_RELATION_FIELDS = {
    "history": {
        "related_name": "history",
        "model_name": "history",
        "headers": ["ID", "History Date", "History Type", "History User"],
        "fields": ["history_id", "history_date", "history_type", "history_user"],
    },
}

OPERATIONAL_EXCEPTION_TABLE_VIEWS = CustomTableView(
    model=OperationalException,
    model_name="operational_exception",
    fields=OPERATIONAL_EXCEPTION_MODEL_FIELDS,
    model_relation_headers=OPERATIONAL_EXCEPTION_MODEL_RELATION_HEADERS,
    model_relation_fields=OPERATIONAL_EXCEPTION_MODEL_RELATION_FIELDS,
    search_fields_list=OPERATIONAL_EXCEPTION_SEARCH_FIELDS,
)

OPERATIONAL_EXCEPTION_VIEWS = CRUDView(
    model=OperationalException,
    model_name="operational_exceptions",
    model_service=OperationalExceptionService,
    model_form=OperationalExceptionForm,
    model_table_view=OPERATIONAL_EXCEPTION_TABLE_VIEWS,
)
