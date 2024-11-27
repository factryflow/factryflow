from datetime import datetime

from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied
from django.db import transaction

from job_manager.models import (
    Dependency,
    Job,
    JobStatusChoices,
    JobType,
)


# ------------------------------------------------------------------------------
# Job Type Services
# ------------------------------------------------------------------------------


class JobTypeService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self,
        name: str,
        external_id: str = "",
        notes: str = "",
        custom_fields: dict = None,
    ) -> JobType:
        # check for permission to create job type
        if not self.permission_service.check_for_permission("add_jobtype"):
            raise PermissionDenied()

        job_type = JobType.objects.create(
            name=name, external_id=external_id, notes=notes, custom_fields=custom_fields
        )
        job_type.full_clean()
        job_type.save(user=self.user)

        return job_type

    @transaction.atomic
    def update(self, job_type: JobType, data: dict) -> JobType:
        # check for permission to update job type
        if not self.permission_service.check_for_permission("change_jobtype"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "notes",
            "custom_fields",
        ]

        job_type, _ = model_update(
            instance=job_type, fields=fields, data=data, user=self.user
        )

        return job_type

    @transaction.atomic
    def delete(self, job_type: JobType) -> None:
        # check for permission to delete job type
        if not self.permission_service.check_for_permission("delete_jobtype"):
            raise PermissionDenied()

        job_type.delete()
        return True


# ------------------------------------------------------------------------------
# Job Services
# ------------------------------------------------------------------------------


class JobService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        name: str,
        due_date: datetime,
        job_type: JobType,
        job_status: JobStatusChoices,
        dependencies: list[Dependency] = None,
        customer: str = "",
        description: str = "",
        external_id: str = "",
        notes: str = "",
        priority: int = None,
        custom_fields: dict = None,
    ) -> Job:
        # check for permission to create job
        if not self.permission_service.check_for_permission("add_job"):
            raise PermissionDenied()

        # get last job and update priority by 1 from last job priority
        last_job = Job.objects.order_by("id").last()
        priority = last_job.priority + 1 if last_job else 1

        job = Job.objects.create(
            name=name,
            due_date=due_date,
            job_type=job_type,
            customer=customer,
            priority=priority,
            job_status=job_status,
            external_id=external_id,
            notes=notes,
            description=description,
            custom_fields=custom_fields,
        )

        job.full_clean()
        job.save(user=self.user)

        if priority:
            job.update_priority(priority)

        if dependencies:
            job.dependencies.set(dependencies)

        return job

    @transaction.atomic
    def update(self, job: Job, data: dict) -> Job:
        # check for permission to update job
        if not self.permission_service.check_for_permission("change_job"):
            raise PermissionDenied()

        fields = [
            "name",
            "due_date",
            "job_type",
            "customer",
            "description",
            "external_id",
            "notes",
            "dependencies",
            "custom_fields",
        ]

        job, _ = model_update(instance=job, fields=fields, data=data, user=self.user)

        # update job priority
        if data.get("priority", None):
            job.update_priority(data["priority"])

        return job

    @transaction.atomic
    def delete(self, job: Job) -> None:
        # check for permission to delete job
        if not self.permission_service.check_for_permission("delete_job"):
            raise PermissionDenied()

        job.delete()
        return True
