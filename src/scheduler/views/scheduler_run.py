from django.urls import reverse
from django.http import HttpResponse
from common.views import CRUDView, CustomTableView
from django_q.tasks import async_task
import datetime

# Create your views here.
from scheduler.models import (
    ResourceAllocations,
    ResourceIntervals,
    SchedulerRuns,
    SchedulerStatusChoices,
)
from scheduler.forms import SchedulerRunsForm
from scheduler.services import SchedulerRunsService

from common.utils.views import (
    add_notification_headers,
)


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


SCHEDULER_RUNS_TABLE_VIEW = CustomTableView(
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

SCHEDULER_RUNS_VIEW = CRUDView(
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
        # Create initial scheduler run record with STARTED status
        scheduler_run = SchedulerRuns.objects.create(
            start_time=datetime.datetime.now(datetime.timezone.utc),
            status=SchedulerStatusChoices.STARTED,
            details="Scheduler run started",
        )

        async_task("scheduler.utils.start_scheduler_run", request.user, scheduler_run)
        if request.htmx:
            response = HttpResponse(status=204)
            response = add_notification_headers(
                response,
                f"The Scheduler has been started. You will be notified when it's done.",
                "success",
            )
            response["HX-Redirect"] = reverse("scheduler_runs") + f"?start_time=desc"
            return response
    except Exception as e:
        raise e

    return HttpResponse(
        {"status": "success", "message": "Scheduler run started successfully."}
    )
