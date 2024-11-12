"""Utility functions for the job_manager app."""

from job_manager.models.job import Job
from job_manager.models.task import Task


def consolidate_parent_task_datetimes():
    """Consolidate the start and end dates of parent tasks."""
    consolidated_tasks = []
    tasks = Task.objects.filter(sub_tasks__isnull=False)

    for task in tasks:
        task.consolidate_start_end_dates()
        consolidated_tasks.append(task)
    
    return consolidated_tasks


def consolidate_job_datetimes():
    """Consolidate the start and end dates of jobs."""
    consolidated_jobs = []
    tasks = Job.objects.filter(tasks__isnull=False)

    for job in tasks:
        job.consolidate_start_end_dates()
        consolidated_jobs.append(job)
    
    return consolidated_jobs
