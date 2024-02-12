from django.shortcuts import render
from common.views import CRUDView, CustomTableView

# Create your views here.
from .models import WeeklyShiftTemplate, OperationalException, OperationalExceptionType
from .forms import WeeklyShiftTemplateForm, OperationalExceptionForm
from .services import WeeklyShiftTemplateService, OperationalExceptionService


# ------------------------------------------------------------------------------
# Weekly Shift Template VIEWS
# ------------------------------------------------------------------------------

WEEKLY_SHIFT_TEMPLATE_MODEL_FIELDS = ["id", "name", "external_id", "notes"]
WEEKLY_SHIFT_TEMPLATE_SEARCH_FIELDS = ["name", "id"]
WEEKLY_SHIFT_TEMPLATE_TABLE_HEADERS = ["ID", "Weekly Shift Template Name", "External ID", "Notes"]

WeeklyShiftTemplateTableView = CustomTableView(
    model=WeeklyShiftTemplate,
    model_name="weekly_shift_template",
    fields=WEEKLY_SHIFT_TEMPLATE_MODEL_FIELDS,
    headers=WEEKLY_SHIFT_TEMPLATE_TABLE_HEADERS,
    search_fields_list=WEEKLY_SHIFT_TEMPLATE_SEARCH_FIELDS,
)

WEEKLY_SHIFT_TEMPLATE_VIEWS = CRUDView(
    model=WeeklyShiftTemplate,
    model_name="weekly_shift_template",
    model_service=WeeklyShiftTemplateService,
    model_form=WeeklyShiftTemplateForm,
    model_table_view=WeeklyShiftTemplateTableView,
)


# ------------------------------------------------------------------------------
# Operational Exception VIEWS
# ------------------------------------------------------------------------------

OPERATIONAL_EXCEPTION_MODEL_FIELDS = ["id", "name", "external_id", "notes"]
OPERATIONAL_EXCEPTION_SEARCH_FIELDS = ["name", "id"]
OPERATIONAL_EXCEPTION_TABLE_HEADERS = ["ID", "Operational Exception Name", "External ID", "Notes"]

OperationalExceptionTableView = CustomTableView(
    model=OperationalException,
    model_name="operational_exception",
    fields=OPERATIONAL_EXCEPTION_MODEL_FIELDS,
    headers=OPERATIONAL_EXCEPTION_TABLE_HEADERS,
    search_fields_list=OPERATIONAL_EXCEPTION_SEARCH_FIELDS,
)

OPERATIONAL_EXCEPTION_VIEWS = CRUDView(
    model=OperationalException,
    model_name="operational_exception",
    model_service=OperationalExceptionService,
    model_form=OperationalExceptionForm,
    model_table_view=OperationalExceptionTableView,
)

