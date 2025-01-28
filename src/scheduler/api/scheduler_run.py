from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_q.tasks import async_task

from scheduler.utils import start_scheduler_run
from common.utils.views import (
    add_notification_headers,
)

from ..models import (
    ResourceAllocations,
    ResourceIntervals,
    SchedulerLog,
    SchedulerRuns,
    SchedulerStatusChoices,
)


@transaction.atomic
def save_scheduler_run(
    scheduled_task,
    scheduler_details,
    scheduler_logs,
    scheduler_start_time,
    scheduler_end_time,
    scheduler_status,
):
    """
    Save a new scheduler run.
    """
    try:
        run_duration = scheduler_end_time - scheduler_start_time

        scheduler_run = SchedulerRuns.objects.create(
            start_time=scheduler_start_time,
            end_time=scheduler_end_time,
            run_duration=run_duration,
            details=scheduler_details,
            status=scheduler_status,
        )

        SchedulerLog.objects.create(
            scheduler_run=scheduler_run,
            logs=scheduler_logs,
        )

        if scheduler_status == SchedulerStatusChoices.COMPLETED:
            for task in scheduled_task:
                assigned_resources = task.get("assigned_resource_ids", [])
                if assigned_resources:
                    for resource_id in assigned_resources:
                        # store resource allocations
                        ResourceAllocations.objects.create(
                            resource_id=resource_id,
                            task_id=task["task_id"],
                            run_id=scheduler_run,
                        )
                        # store resource intervals
                        ResourceIntervals.objects.create(
                            resource_id=resource_id,
                            task_id=task["task_id"],
                            run_id=scheduler_run,
                            interval_start=task.get("planned_task_start"),
                            interval_end=task.get("planned_task_end"),
                        )

    except Exception as e:
        raise e


@csrf_exempt
def start_scheduler_run_api_view(request):
    """
    Start a new scheduler run in background.
    """
    try:
        print("heellll")
        # start_scheduler_run(request)
        background_task_id = async_task("scheduler.utils.start_scheduler_run", request)
        response = HttpResponse(status=202)
        add_notification_headers(
            response,
            f"The Scheduler has been started. You will be notified when it's done. {background_task_id}",
            "success",
        )

        return response
    except Exception as e:
        response = HttpResponse(status=500)
        add_notification_headers(
            response,
            f"Error: str(e)" "error",
        )

        return response
