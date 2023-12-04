from django.db import transaction

from job_manager.models import JobType


@transaction.atomic
def job_type_create(*, name: str) -> JobType:
    job_type = JobType(name=name)
    job_type.full_clean()
    job_type.save()

    return job_type
