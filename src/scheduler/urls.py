from django.urls import path

from .api.scheduler_logs import SchedulerLogsAPIView
from .api.scheduler_run import start_scheduler_run
from .views import ResourceIntervals_VIEWS, SchedulerRuns_VIEWS

urlpatterns = [
    # scheduler runs urls
    path(
        "scheduler-runs/", SchedulerRuns_VIEWS.get_all_instances, name="scheduler_runs"
    ),
    path(
        "scheduler-runs/view/<int:id>/",
        SchedulerRuns_VIEWS.show_model_form,
        name="view_scheduler_runs",
    ),
    path(
        "scheduler-runs/view/<int:id>/field=<str:field>",
        SchedulerRuns_VIEWS.show_model_form,
        name="scheduler_runs_relationships",
    ),
    # resource intervals urls
    path(
        "resource-intervals/",
        ResourceIntervals_VIEWS.get_all_instances,
        name="resource_intervals",
    ),
    path(
        "resource-intervals/view/<int:id>/",
        ResourceIntervals_VIEWS.show_model_form,
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
