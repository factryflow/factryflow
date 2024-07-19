from common.views import CRUDView, CustomTableView

# Create your views here.
from .models import *
from .forms import *
from .services import *


# ------------------------------------------------------------------------------
# Weekly Shift Template VIEWS
# ------------------------------------------------------------------------------

WEEKLY_SHIFT_TEMPLATE_MODEL_FIELDS = ["id", "name", "external_id", "notes"]
WEEKLY_SHIFT_TEMPLATE_SEARCH_FIELDS = ["name", "id"]
WEEKLY_SHIFT_TEMPLATE_TABLE_HEADERS = [
    "ID",
    "Weekly Shift Template Name",
    "External ID",
    "Notes",
]

WEEKLY_SHIFT_TEMPLATE_MODEL_RELATION_HEADERS = [
    "WEEKLY SHIFT TEMPLATE DETAILS",
    "HISTORY",
]

WEEKLY_SHIFT_TEMPLATE_MODEL_RELATION_FIELDS = {
    "weekly_shift_template_details": [
        "weekly_shift_template_details",
        ["ID", "Day of Week", "Start Time", "End Time"],
        ["id", "day_of_week", "start_time", "end_time"],
    ],
    "history": [
        "history",
        ["ID", "History Date", "History Type", "History User"],
        ["id", "history_date", "history_type", "history_user"],
    ],
}

SHIFT_TEMPLATE_DETAILS_FORMSET_FORM_FIELDS = ["day_of_week", "start_time", "end_time"]

SHIFT_TEMPLATE_DETAILS_FORMSET_OPTIONS = [
    WeeklyShiftTemplateDetail,
    WeeklyShiftTemplateDetailForm,
    "weekly_shift_template_details",
    SHIFT_TEMPLATE_DETAILS_FORMSET_FORM_FIELDS,
]


WeeklyShiftTemplateTableView = CustomTableView(
    model=WeeklyShiftTemplate,
    model_name="weekly_shift_template",
    fields=WEEKLY_SHIFT_TEMPLATE_MODEL_FIELDS,
    headers=WEEKLY_SHIFT_TEMPLATE_TABLE_HEADERS,
    search_fields_list=WEEKLY_SHIFT_TEMPLATE_SEARCH_FIELDS,
    model_relation_headers=WEEKLY_SHIFT_TEMPLATE_MODEL_RELATION_HEADERS,
    model_relation_fields=WEEKLY_SHIFT_TEMPLATE_MODEL_RELATION_FIELDS,
)

WEEKLY_SHIFT_TEMPLATE_VIEWS = CRUDView(
    model=WeeklyShiftTemplate,
    model_name="weekly_shift_template",
    model_service=WeeklyShiftTemplateService,
    model_form=WeeklyShiftTemplateForm,
    model_table_view=WeeklyShiftTemplateTableView,
    formset_options=SHIFT_TEMPLATE_DETAILS_FORMSET_OPTIONS,
)


# ------------------------------------------------------------------------------
# Weekly Shift Template Detail VIEWS
# ------------------------------------------------------------------------------

WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_FIELDS = [
    "id",
    "day_of_week",
    "start_time",
    "end_time",
]
WEEKLY_SHIFT_TEMPLATE_DETAIL_SEARCH_FIELDS = ["day_of_week", "id"]
WEEKLY_SHIFT_TEMPLATE_DETAIL_TABLE_HEADERS = [
    "ID",
    "Day of Week",
    "Start Time",
    "End Time",
]

WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_RELATION_HEADERS = ["HISTORY"]
WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_RELATION_FIELDS = {
    "history": [
        "history",
        ["ID", "History Date", "History Type", "History User"],
        ["id", "history_date", "history_type", "history_user"],
    ],
}

WeeklyShiftTemplateDetailTableView = CustomTableView(
    model=WeeklyShiftTemplateDetail,
    model_name="weekly_shift_template_detail",
    fields=WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_FIELDS,
    headers=WEEKLY_SHIFT_TEMPLATE_DETAIL_TABLE_HEADERS,
    model_relation_headers=WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_RELATION_HEADERS,
    model_relation_fields=WEEKLY_SHIFT_TEMPLATE_DETAIL_MODEL_RELATION_FIELDS,
    search_fields_list=WEEKLY_SHIFT_TEMPLATE_DETAIL_SEARCH_FIELDS,
)

WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS = CRUDView(
    model=WeeklyShiftTemplateDetail,
    model_name="weekly_shift_template_detail",
    model_service=WeeklyShiftTemplateDetailService,
    model_form=WeeklyShiftTemplateDetailForm,
    model_table_view=WeeklyShiftTemplateDetailTableView,
)


# ------------------------------------------------------------------------------
# Operational Exception Type VIEWS
# ------------------------------------------------------------------------------

OPERATIONAL_EXCEPTION_TYPE_MODEL_FIELDS = ["id", "name", "external_id", "notes"]
OPERATIONAL_EXCEPTION_TYPE_SEARCH_FIELDS = ["name", "id"]
OPERATIONAL_EXCEPTION_TYPE_TABLE_HEADERS = [
    "ID",
    "Operational Exception Type Name",
    "External ID",
    "Notes",
]

OPERATIONAL_EXCEPTION_TYPE_MODEL_RELATION_HEADERS = ["HISTORY"]
OPERATIONAL_EXCEPTION_TYPE_MODEL_RELATION_FIELDS = {
    "history": [
        "history",
        ["ID", "History Date", "History Type", "History User"],
        ["id", "history_date", "history_type", "history_user"],
    ],
}

OperationalExceptionTypeTableView = CustomTableView(
    model=OperationalExceptionType,
    model_name="operational_exception_type",
    fields=OPERATIONAL_EXCEPTION_TYPE_MODEL_FIELDS,
    headers=OPERATIONAL_EXCEPTION_TYPE_TABLE_HEADERS,
    model_relation_headers=OPERATIONAL_EXCEPTION_TYPE_MODEL_RELATION_HEADERS,
    model_relation_fields=OPERATIONAL_EXCEPTION_TYPE_MODEL_RELATION_FIELDS,
    search_fields_list=OPERATIONAL_EXCEPTION_TYPE_SEARCH_FIELDS,
)

OPERATIONAL_EXCEPTION_TYPE_VIEWS = CRUDView(
    model=OperationalExceptionType,
    model_name="operational_exception_type",
    model_service=OperationalExceptionTypeService,
    model_form=OperationalExceptionTypeForm,
    model_table_view=OperationalExceptionTypeTableView,
)


# ------------------------------------------------------------------------------
# Operational Exception VIEWS
# ------------------------------------------------------------------------------

OPERATIONAL_EXCEPTION_MODEL_FIELDS = [
    "id",
    "external_id",
    "start_datetime",
    "end_datetime",
    "operational_exception_type",
    "weekly_shift_template",
    "resource",
    "notes",
]

OPERATIONAL_EXCEPTION_SEARCH_FIELDS = [
    "id",
    "external_id",
    "start_datetime",
    "end_datetime",
    "operational_exception_type",
    "weekly_shift_template",
    "resource",
    "notes",
]

OPERATIONAL_EXCEPTION_TABLE_HEADERS = [
    "ID",
    "External ID",
    "Start Datetime",
    "End Datetime",
    "Operational Exception Type",
    "Weekly Shift Template",
    "Resource",
    "Notes",
]

OPERATIONAL_EXCEPTION_MODEL_RELATION_HEADERS = ["HISTORY"]
OPERATIONAL_EXCEPTION_MODEL_RELATION_FIELDS = {
    "history": [
        "history",
        ["ID", "History Date", "History Type", "History User"],
        ["id", "history_date", "history_type", "history_user"],
    ],
}

OperationalExceptionTableView = CustomTableView(
    model=OperationalException,
    model_name="operational_exception",
    fields=OPERATIONAL_EXCEPTION_MODEL_FIELDS,
    headers=OPERATIONAL_EXCEPTION_TABLE_HEADERS,
    model_relation_headers=OPERATIONAL_EXCEPTION_MODEL_RELATION_HEADERS,
    model_relation_fields=OPERATIONAL_EXCEPTION_MODEL_RELATION_FIELDS,
    search_fields_list=OPERATIONAL_EXCEPTION_SEARCH_FIELDS,
)

OPERATIONAL_EXCEPTION_VIEWS = CRUDView(
    model=OperationalException,
    model_name="operational_exception",
    model_service=OperationalExceptionService,
    model_form=OperationalExceptionForm,
    model_table_view=OperationalExceptionTableView,
)
