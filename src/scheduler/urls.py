from django.urls import path

from .api.scheduler_logs import SchedulerLogsAPIView
from .api.scheduler_run import start_scheduler_run_api_view
from .views import RESOURCE_INTERVAL_VIEW, SCHEDULER_RUNS_VIEW, start_scheduler_run_view

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
    path("scheduler-runs/start/", start_scheduler_run_view, name="start_scheduler_run"),
    path("api/scheduler-runs/start/", start_scheduler_run_api_view, name="start_scheduler_run_api"),
    path(
        "scheduler-logs/view/<int:scheduler_run_id>/",
        SchedulerLogsAPIView.as_view(),
        name="get_scheduler_logs",
    ),
]
