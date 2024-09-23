from common.views import CRUDView, CustomTableView

# Create your views here.
from .models import (
    OperationalException,
    OperationalExceptionType,
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
    DaysOfWeek,
)
from .forms import *
from .services import *


# ------------------------------------------------------------------------------
# Weekly Shift Template VIEWS
# ------------------------------------------------------------------------------

WEEKLY_SHIFT_TEMPLATE_MODEL_FIELDS = ["id", "name", "notes"]
WEEKLY_SHIFT_TEMPLATE_SEARCH_FIELDS = ["name", "id"]
WEEKLY_SHIFT_TEMPLATE_TABLE_HEADERS = [
    "ID",
    "Weekly Shift Template Name",
    "Notes",
]

WEEKLY_SHIFT_TEMPLATE_MODEL_RELATION_HEADERS = [
    "TEMPLATE DETAILS",
    "HISTORY",
]

WEEKLY_SHIFT_TEMPLATE_MODEL_RELATION_FIELDS = {
    "template_details": {
        "related_name": "weekly_shift_template_details",
        "model_name": "weekly_shift_template_detail",
        "headers": ["ID", "Day of Week", "Start Time", "End Time"],
        "fields": ["id", "day_of_week", "start_time", "end_time"],
        "select_fields": {
            "day_of_week": dict(DaysOfWeek.choices),
        },
        "relationship_fields": "weekly_shift_template",
        "show_edit_actions": True,
    },
    "history": {
        "related_name": "history",
        "model_name": "history",
        "headers": ["ID", "History Date", "History Type", "History User"],
        "fields": ["history_id", "history_date", "history_type", "history_user"],
        "show_edit_actions": False,
    },
}

SHIFT_TEMPLATE_DETAILS_FORMSET_FORM_FIELDS = ["day_of_week", "start_time", "end_time"]

SHIFT_TEMPLATE_DETAILS_FORMSET_OPTIONS = [
    WeeklyShiftTemplateDetail,
    WeeklyShiftTemplateDetailForm,
    "weekly_shift_template_details",
    SHIFT_TEMPLATE_DETAILS_FORMSET_FORM_FIELDS,
    "weekly_shift_template_details",
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
    model_name="weekly_shift_templates",
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
    "history": {
        "related_name": "history",
        "model_name": "history",
        "headers": ["ID", "History Date", "History Type", "History User"],
        "fields": ["history_id", "history_date", "history_type", "history_user"],
    },
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
    model_name="weekly_shift_template_details",
    model_service=WeeklyShiftTemplateDetailService,
    model_form=WeeklyShiftTemplateDetailForm,
    model_table_view=WeeklyShiftTemplateDetailTableView,
    sub_model_relation=True,
)


# ------------------------------------------------------------------------------
# Operational Exception Type VIEWS
# ------------------------------------------------------------------------------

OPERATIONAL_EXCEPTION_TYPE_MODEL_FIELDS = ["id", "name", "notes"]
OPERATIONAL_EXCEPTION_TYPE_SEARCH_FIELDS = ["name", "id"]
OPERATIONAL_EXCEPTION_TYPE_TABLE_HEADERS = [
    "ID",
    "Operational Exception Type Name",
    "Notes",
]

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
    model_name="operational_exception_types",
    model_service=OperationalExceptionTypeService,
    model_form=OperationalExceptionTypeForm,
    model_table_view=OperationalExceptionTypeTableView,
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
    "start_datetime",
    "end_datetime",
    "operational_exception_type",
    "weekly_shift_template",
    "resource",
    "notes",
]

OPERATIONAL_EXCEPTION_TABLE_HEADERS = [
    "ID",
    "Resource",
    "Operational Exception Type",
    "Weekly Shift Template",
    "Start Datetime",
    "End Datetime",
    "Notes",
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
    model_name="operational_exceptions",
    model_service=OperationalExceptionService,
    model_form=OperationalExceptionForm,
    model_table_view=OperationalExceptionTableView,
)
