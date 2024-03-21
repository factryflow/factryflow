from django.shortcuts import render
from common.views import CRUDView, CustomTableView

# Create your views here.
from .models import ResourceAllocations, ResourceIntervals, SchedulerRuns, SchedulerStatusChoices
from .forms import ResourceIntervalsForm, SchedulerRunsForm
from .services import ResourceIntervalsService, SchedulerRunsService




# ------------------------------------------------------------------------------
# Scheduler Runs VIEWS
# ------------------------------------------------------------------------------

SCHEDULER_TAILWIND_CLASSES = {
    "ST": "bg-haxyellow text-[#F6C000]",
    "CP": "bg-haxgreen text-[#3DAD99]",
    "FL": "bg-haxred text-[#FF4D4F]",
    "CN": "bg-haxpurple text-[#7239EA]",
}

SCHEDULER_STATUS =  {
    "ST": "Started",
    "CP": "Completed",
    "FL": "Failed",
    "CN": "Cancelled",
}

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
SCHEDULER_TABLE_HEADERS = [
    "Run ID",
    "Start Time",
    "End Time",
    "Run Duration",
    "Details",
    "Status",
]

SCHEDULER_MODEL_RELATION_HEADERS = ["RESOURCE_ALLOCATIONS", "RESOURCE_INTERVALS"]

SCHEDULER_MODEL_RELATION_FIELDS = {
    # model_name: [model, related_name, [headers], [fields]]
    "resource_allocations": [ResourceAllocations, "run_id", ["Resource", "Task"], ["resource", "task"]],
    "resource_intervals": [ResourceIntervals, "run_id", ["Resource", "Task", "Interval Start", "Interval End"], ["resource", "task", "interval_start", "interval_end"]],
}


SchedulerRunsView = CustomTableView(
    model=SchedulerRuns,
    model_name="scheduler_runs",
    fields=SCHEDULER_MODEL_FIELDS,
    status_choices_class=SchedulerStatusChoices,
    headers=SCHEDULER_TABLE_HEADERS,
    tailwind_classes=SCHEDULER_TAILWIND_CLASSES,
    search_fields_list=SCHEDULER_SEARCH_FIELDS,
    model_relation_headers=SCHEDULER_MODEL_RELATION_HEADERS,
    model_relation_fields=SCHEDULER_MODEL_RELATION_FIELDS,
    status_classes=SCHEDULER_STATUS,
)

SchedulerRuns_VIEWS = CRUDView(
    model=SchedulerRuns,
    model_name="scheduler_runs",
    model_form=SchedulerRunsForm,
    model_service=SchedulerRunsService,
    model_table_view=SchedulerRunsView,
    view_only=True,
    button_text="Run Scheduler",
    cud_actions_rule=False,
)


# ------------------------------------------------------------------------------
# Resource Intervals VIEWS
# ------------------------------------------------------------------------------

RESOURCE_INTERVALS_MODEL_FIELDS = [
    "resource",
    "task",
    "interval_start",
    "interval_end",
]

RESOURCE_INTERVALS_SEARCH_FIELDS = ["resource", "task"]
RESOURCE_INTERVALS_TABLE_HEADERS = [
    "Resource",
    "Task",
    "Interval Start",
    "Interval End",
]

ResourceIntervalsView = CustomTableView(
    model=ResourceIntervals,
    model_name="resource_intervals",
    fields=RESOURCE_INTERVALS_MODEL_FIELDS,
    headers=RESOURCE_INTERVALS_TABLE_HEADERS,
    search_fields_list=RESOURCE_INTERVALS_SEARCH_FIELDS,
)


ResourceIntervals_VIEWS = CRUDView(
    model=ResourceIntervals,
    model_name="resource_intervals",
    model_form=ResourceIntervalsForm,
    model_service=ResourceIntervalsService,
    model_table_view=ResourceIntervalsView,
    cud_actions_rule=False,
)