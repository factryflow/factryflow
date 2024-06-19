import datetime

from django.http import HttpResponse
from django.urls import reverse
from job_manager.models import Task

from .models import (
    ResourceAllocations,
    ResourceIntervals,
    SchedulerRuns,
    SchedulerStatusChoices,
)
from .services import (
    SchedulingService,
)


# # scheduler router
# scheduler_router = Router()
def save_scheduler_run(
    scheduled_task,
    scheduler_details,
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

        scheduler_run.save()

        if scheduler_status == SchedulerStatusChoices.COMPLETED:
            for task in scheduled_task:
                task_obj = Task.objects.get(id=task["task_id"])
                for resource_id in task["assigned_resource_ids"]:
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
                        interval_start=task.get("task_start").isoformat(),
                        interval_end=task.get("task_end").isoformat(),
                    )

    except Exception as e:
        # raise the error as exception
        raise e


def start_scheduler_run(request):
    """
    Start a new scheduler run in background.
    """
    scheduler_start_time = datetime.datetime.now(datetime.timezone.utc)
    try:
        scheduled_task = SchedulingService(horizon_weeks=5).run()
        scheduler_end_time = datetime.datetime.now(datetime.timezone.utc)

        # check if the scheduleed task has error key
        if "error" in scheduled_task:
            scheduler_status = SchedulerStatusChoices.FAILED
            scheduler_details = scheduled_task["error"]

        else:
            scheduler_status = SchedulerStatusChoices.COMPLETED
            scheduler_details = "Scheduler run completed successfully."

        save_scheduler_run(
            scheduled_task,
            scheduler_details,
            scheduler_start_time,
            scheduler_end_time,
            scheduler_status,
        )

        if request.htmx:
            headers = {"HX-Redirect": reverse("scheduler_runs")}
            response = HttpResponse(status=204, headers=headers)
            return response

    except Exception as e:
        # raise the error as exception
        raise e

    return {"status": "success", "message": "Scheduler run started successfully."}
