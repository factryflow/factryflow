from common.utils.services import build_or_retrieve_instance
from django.db import transaction

from job_manager.models.job import Job, JobStatus, JobType


@transaction.atomic
def job_type_create(*, name: str) -> JobType:
    job_type = JobType(name=name)
    job_type.full_clean()
    job_type.save()

    return job_type


@transaction.atomic
def job_create_or_update(
    *, job_data: dict, job_type: JobType, job_status: JobStatus
) -> Job:
    job = build_or_retrieve_instance(Job, job_data)

    job.job_type = job_type
    job.job_status = job_status

    job.full_clean()
    job.save()

    return job
