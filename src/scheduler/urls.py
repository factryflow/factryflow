from django.urls import path

from scheduler.api.scheduler_logs import SchedulerLogsAPIView
from scheduler.api.scheduler_run import start_scheduler_run
from scheduler.views import RESOURCE_INTERVAL_VIEW, SCHEDULER_RUNS_VIEW

urlpatterns = [
    # scheduler runs urls
    path(
        "scheduler-runs/", SCHEDULER_RUNS_VIEW.get_all_instances, name="scheduler_runs"
    ),
    path(
        "scheduler-runs/view/<int:id>/",
        SCHEDULER_RUNS_VIEW.show_model_form,
        name="view_scheduler_runs",
    ),
    path(
        "scheduler-runs/view/<int:id>/field=<str:field>",
        SCHEDULER_RUNS_VIEW.show_model_form,
        name="scheduler_runs_relationships",
    ),
    # resource intervals urls
    path(
        "resource-intervals/",
        RESOURCE_INTERVAL_VIEW.get_all_instances,
        name="resource_intervals",
    ),
    path(
        "resource-intervals/view/<int:id>/",
        RESOURCE_INTERVAL_VIEW.show_model_form,
        name="view_resource_intervals",
    ),
    # Scheduler Run route
    path("scheduler-runs/start/", start_scheduler_run, name="start_scheduler_run"),
    path(
        "scheduler-logs/view/<int:scheduler_run_id>/",
        SchedulerLogsAPIView.as_view(),
        name="get_scheduler_logs",
    ),
]
