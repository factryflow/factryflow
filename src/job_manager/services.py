from datetime import datetime

from common.services import model_update
from common.utils.services import build_or_retrieve_instance
from django.db import transaction
from django.shortcuts import get_object_or_404

from job_manager.models import (
    Dependency,
    DependencyType,
    Job,
    JobType,
    Task,
    TaskType,
    WorkCenter,
)

# ------------------------------------------------------------------------------
# Task Services
# ------------------------------------------------------------------------------


@transaction.atomic
def task_type_create_or_update(task_type_data: dict) -> TaskType:
    task_type, _ = build_or_retrieve_instance(TaskType, task_type_data)

    task_type.full_clean()
    task_type.save()

    return task_type


@transaction.atomic
def task_create_or_update(
    *,
    task_data: dict,
    task_type: TaskType = None,
    work_center: WorkCenter = None,
    job: Job = None,
    predecessors: list[Task] = None,
    successors: list[Task] = None,
    dependencies: list[Dependency] = None,
) -> Task:
    task, _ = build_or_retrieve_instance(
        Task,
        task_data,
        allowed_fields=[
            "id",
            "external_id",
            "name",
            "setup_time",
            "run_time_per_unit",
            "teardown_time",
            "quantity",
            "item",
        ],
    )

    # set foreign keys if provided
    if task_type is not None:
        task.task_type = task_type

    if work_center is not None:
        task.work_center = work_center

    if job is not None:
        task.job = job

    if dependencies is not None:
        task.dependencies.set(dependencies)

    if predecessors is not None:
        task.predecessors.set(predecessors)

    if successors is not None:
        task.successors.set(successors)

    # todo - update assignment rule

    task.full_clean()
    task.save()

    return task


# ------------------------------------------------------------------------------
# Job Services
# ------------------------------------------------------------------------------


@transaction.atomic
def job_type_create_or_update(job_type_data: dict) -> JobType:
    job_type, _ = build_or_retrieve_instance(JobType, job_type_data)
    job_type.full_clean()
    job_type.save()

    return job_type


class JobService:
    def __init__(self):
        pass

    @transaction.atomic
    def create(
        name: str,
        due_date: datetime,
        job_type: JobType,
        customer: str = "",
        description: str = "",
        external_id: str = "",
        note: str = "",
        priority: int = None,
    ):
        job = Job.objects.create(
            name=name,
            due_date=due_date,
            job_type=job_type,
            customer=customer,
            external_id=external_id,
            note=note,
            description=description,
        )

        job.full_clean()
        job.save()

        job.update_priority(priority)

        return job

    @transaction.atomic
    def update(job: Job, data: dict):
        fields = [
            "name",
            "due_date",
            "job_type",
            "customer",
            "description",
            "external_id",
            "note",
            "dependencies",
        ]

        job, _ = model_update(instance=job, fields=fields, data=data)

        # update job priority
        if data.get("priority", None):
            job.update_priority(data["priority"])

        return job

    @transaction.atomic
    def delete(job: Job):
        job.delete()


@transaction.atomic
def job_create_or_update(
    *, job_data: dict, job_type: JobType = None, dependencies: list[Dependency] = None
) -> Job:
    job, _ = build_or_retrieve_instance(
        Job,
        job_data,
        allowed_fields=[
            "id",
            "name",
            "description",
            "customer",
            "due_date",
            "external_id",
            "note",
            "job_status",
        ],
    )

    if job_type is not None:
        job.job_type = job_type

    if dependencies is not None:
        job.dependencies.set(dependencies)

    job.full_clean()
    job.save()

    # update job priority
    if job_data.get("priority", None):
        job.update_priority(job_data["priority"])

    return job


def job_list(id: int = None):
    """
    Gets all job data including related values from job_status model.
    If an id is provided, returns the job data with that ID.
    Otherwise, returns all job statuses.
    """
    if id:
        return get_object_or_404(Job.objects.all(), id=id)
    else:
        return Job.objects.all()


@transaction.atomic
def job_delete(id: int):
    job = job_list(id=id)
    job.delete()


# ------------------------------------------------------------------------------
# Dependency Services
# ------------------------------------------------------------------------------


@transaction.atomic
def dependency_type_create_or_update(dependency_type_data: dict) -> DependencyType:
    dependency_type, _ = build_or_retrieve_instance(
        DependencyType, dependency_type_data
    )
    dependency_type.full_clean()
    dependency_type.save()

    return dependency_type


@transaction.atomic
def dependency_create_or_update(
    *,
    dependency_data: dict,
    dependency_type: DependencyType = None,
    tasks: list[Task] = None,
    jobs: list[Job] = None,
) -> Dependency:
    dependency, _ = build_or_retrieve_instance(
        Dependency,
        dependency_data,
        allowed_fields=[
            "id",
            "name",
            "external_id",
            "expected_close_datetime",
            "notes",
        ],
    )

    if dependency_type is not None:
        dependency.dependency_type = dependency_type

    if tasks is not None:
        dependency.tasks.set(tasks)

    if jobs is not None:
        dependency.jobs.set(jobs)

    dependency.full_clean()
    dependency.save()

    return dependency
