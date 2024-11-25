import datetime

from django.db import transaction
from job_manager.models.task import Task
from job_manager.utils import (
    consolidate_job_datetimes,
    consolidate_parent_task_datetimes,
)

# from scheduler.api.scheduler_run import save_scheduler_run
from scheduler.models import (
    ResourceAllocations,
    ResourceIntervals,
    SchedulerLog,
    SchedulerRuns,
    SchedulerStatusChoices,
)
from scheduler.services import SchedulingService


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


@transaction.atomic
def start_scheduler_run(request):
    """
    Start a new scheduler run in background.
    """
    scheduler_start_time = datetime.datetime.now(datetime.timezone.utc)
    try:
        scheduled_task = SchedulingService(horizon_weeks=5, user=request.user).run(
            selected_tasks=Task.objects.filter(sub_tasks__isnull=True),
        )  # Run the scheduler for the microbatched subtasks
        scheduler_end_time = datetime.datetime.now(datetime.timezone.utc)

        # check if the scheduled task has error key
        if "error" in scheduled_task:
            scheduler_status = SchedulerStatusChoices.FAILED
            scheduler_details = scheduled_task["error"]

        else:
            scheduler_status = SchedulerStatusChoices.COMPLETED
            scheduler_details = "Scheduler run completed successfully."

        scheduler_results = {}
        scheduler_logs = {}

        if "error" in scheduled_task:
            scheduler_results = scheduled_task["error"]
            scheduler_logs = {"scheduler_error": scheduled_task["error"]}

        else:
            scheduler_results = scheduled_task["data"]
            scheduler_logs = scheduled_task["logs"]

        save_scheduler_run(
            scheduler_results,
            scheduler_details,
            scheduler_logs,
            scheduler_start_time,
            scheduler_end_time,
            scheduler_status,
        )
        
        consolidate_parent_task_datetimes()  # Updates the parent Task datetimes based on the Subtask start/end datetimes
        consolidate_job_datetimes()  # Updates the Job datetimes based on the new parent Task datetimes

    except Exception as e:
        # raise the error as exception
        raise e
