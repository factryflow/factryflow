from django.urls import reverse
from django.http import HttpResponse
from common.views import CRUDView, CustomTableView
from django.template.loader import render_to_string

# Create your views here.
from scheduler.models import (
    ResourceAllocations,
    ResourceIntervals,
    SchedulerRuns,
    SchedulerStatusChoices,
)
from scheduler.forms import SchedulerRunsForm
from scheduler.services import SchedulerRunsService
from scheduler.utils import start_scheduler_run


# ------------------------------------------------------------------------------
# Scheduler Runs VIEWS
# ------------------------------------------------------------------------------


SCHEDULER_TAILWIND_CLASSES = {
    "ST": "bg-haxyellow text-[#F6C000]",
    "CP": "bg-haxgreen text-[#3DAD99]",
    "FL": "bg-haxred text-[#FF4D4F]",
    "CN": "bg-haxpurple text-[#7239EA]",
}

SCHEDULER_STATUS = {
    "ST": "loader-template",  # This will be used to reference the loader template
    "CP": "Completed",
    "FL": "Failed",
    "CN": "Cancelled",
}

class SchedulerRunsTableView(CustomTableView):
    def process_cell_value(self, value, field):
        """Process cell value before rendering in table."""
        if field == 'status' and value == 'ST':
            # For Started status, use the loader template
            return '<div class="flex items-center gap-2"><div class="animate-spin rounded-full h-4 w-4 border-2 border-[#F6C000] border-t-transparent"></div><span>Started</span></div>'
        return super().process_cell_value(value, field)

SCHEDULER_MODEL_FIELDS = [
    "id",
    "start_time",
    "end_time",
    "run_duration",
    "details",
    "status",
]

SCHEDULER_STATUS_FILTER_FIELD = "status"
SCHEDULER_SEARCH_FIELDS = ["id", "details", "status"]

SCHEDULER_MODEL_RELATION_HEADERS = [
    "RESOURCE_ALLOCATIONS",
    "RESOURCE_INTERVALS",
    "HISTORY",
]

SCHEDULER_MODEL_RELATION_FIELDS = {
    # model_name: [model, related_name, [headers], [fields]]
    "resource_allocations": {
        "model": ResourceAllocations,
        "model_name": "resource_allocations",
        "related_name": "run_id",
        "headers": ["Resource", "Task"],
        "fields": ["resource", "task"],
        "show_edit_actions": False,
    },
    "resource_intervals": {
        "model": ResourceIntervals,
        "model_name": "resource_intervals",
        "related_name": "run_id",
        "headers": ["Resource", "Task", "Interval Start", "Interval End"],
        "fields": ["resource", "task", "interval_start", "interval_end"],
        "show_edit_actions": False,
    },
    "history": {
        "model": "history",
        "model_name": "history",
        "related_name": "history",
        "headers": [
            "ID",
            "Resource",
            "Interval Start",
            "Interval End",
            "History Date",
            "History Type",
            "History User",
        ],
        "fields": [
            "history_id",
            "resource",
            "interval_start",
            "interval_end",
            "history_date",
            "history_type",
            "history_user",
        ],
        "show_edit_actions": False,
    },
}


SCHEDULER_RUNS_TABLE_VIEW = SchedulerRunsTableView(
    model=SchedulerRuns,
    model_name="scheduler_runs",
    fields=SCHEDULER_MODEL_FIELDS,
    status_choices_class=SchedulerStatusChoices,
    tailwind_classes=SCHEDULER_TAILWIND_CLASSES,
    search_fields_list=SCHEDULER_SEARCH_FIELDS,
    status_filter_field=SCHEDULER_STATUS_FILTER_FIELD,
    model_relation_headers=SCHEDULER_MODEL_RELATION_HEADERS,
    model_relation_fields=SCHEDULER_MODEL_RELATION_FIELDS,
    status_classes=SCHEDULER_STATUS,
)

class SchedulerRunsCRUDView(CRUDView):
    def get_all_instances(self, request):
        context = super().get_all_instances(request)
        # Check if there's any active scheduler run (status = STARTED)
        active_scheduler_run = SchedulerRuns.objects.filter(status=SchedulerStatusChoices.STARTED).exists()
        if isinstance(context, dict):
            context['active_scheduler_run'] = active_scheduler_run
        return context if isinstance(context, dict) else render(request, self.list_template_name, {'active_scheduler_run': active_scheduler_run})

SCHEDULER_RUNS_VIEW = SchedulerRunsCRUDView(
    model=SchedulerRuns,
    model_name="scheduler_runs",
    model_form=SchedulerRunsForm,
    model_service=SchedulerRunsService,
    model_table_view=SCHEDULER_RUNS_TABLE_VIEW,
    view_only=True,
    button_text="Run Scheduler",
    user_rule_permission=False,
    list_template_name="scheduler/list.html",
)


# ------------------------------------------------------------------------------
# Start Scheduler Run View
# ------------------------------------------------------------------------------


def start_scheduler_run_view(request):
    """
    Start a new scheduler run in background.
    """
    try:
        start_scheduler_run(request)
        if request.htmx:
            headers = {"HX-Redirect": reverse("scheduler_runs")}
            response = HttpResponse(status=204, headers=headers)
            # headers = {"HX-Redirect": reverse("scheduler_runs")}
            # response = HttpResponse(status=302, headers=headers)
            return response
    except Exception as e:
        raise e

    return HttpResponse(
        {"status": "success", "message": "Scheduler run started successfully."}
    )
