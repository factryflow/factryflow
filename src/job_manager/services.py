from datetime import datetime

from common.services import model_update
from django.db import transaction
from api.permission_checker import AbstractPermissionService
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
# WorkCenter Services
# ------------------------------------------------------------------------------


class WorkCenterService:
    def __init__(self, user=None):
        self.user = user

    def create(self, name: str, notes: str) -> WorkCenter:
        work_center = WorkCenter.objects.create(name=name, notes=notes)
        work_center.full_clean()
        work_center.save(user=self.user)

        return work_center

    def update(self, work_center: WorkCenter, data: dict) -> WorkCenter:
        fields = [
            "name",
            "notes",
        ]

        work_center, _ = model_update(instance=work_center, fields=fields, data=data, user=self.user)

        return work_center

    def delete(self, work_center: WorkCenter) -> None:
        work_center.delete()


# ------------------------------------------------------------------------------
# Task Type Services
# ------------------------------------------------------------------------------


class TaskTypeService:
    def __init__(self, user=None):
        self.user = user

    def create(self, name: str) -> TaskType:
        task_type = TaskType.objects.create(name=name)
        task_type.full_clean()
        task_type.save(user=self.user)

        return task_type

    def update(self, task_type: TaskType, data: dict) -> TaskType:
        fields = [
            "name",
        ]

        task_type, _ = model_update(instance=task_type, fields=fields, data=data, user=self.user)
        return task_type

    def delete(self, task_type: TaskType) -> None:
        task_type.delete()


# ------------------------------------------------------------------------------
# Task Services
# ------------------------------------------------------------------------------


class TaskService:
    def __init__(self, user=None):
        self.user = user

    @transaction.atomic
    def create(
        self,
        *,
        name: str,
        run_time_per_unit: float,
        quantity: int,
        task_type: TaskType,
        setup_time: float = 0,
        teardown_time: float = 0,
        external_id: str = "",
        notes="",
        work_center: WorkCenter = None,
        job: Job = None,
        dependencies: list[Dependency] = None,
        predecessors: list[Task] = None,
        successors: list[Task] = None,
    ) -> Task:
        task = Task.objects.create(
            name=name,
            external_id=external_id,
            notes=notes,
            setup_time=setup_time,
            run_time_per_unit=run_time_per_unit,
            teardown_time=teardown_time,
            quantity=quantity,
            task_type=task_type,
            work_center=work_center,
            job=job,
        )

        task.full_clean()
        task.save(user=self.user)

        if dependencies:
            task.dependencies.set(dependencies)

        if predecessors:
            task.predecessors.set(predecessors)

        if successors:
            task.successors.set(successors)

        return task

    @transaction.atomic
    def update(self, *, instance: Task, data: dict) -> Task:
        fields = [
            "name",
            "external_id",
            "notes",
            "setup_time",
            "run_time_per_unit",
            "teardown_time",
            "quantity",
            "item",
            "task_type",
            "work_center",
            "job",
            "dependencies",
            "predecessors",
            "successors",
        ]

        task, _ = model_update(instance=instance, fields=fields, data=data, user=self.user)

        return task

    @transaction.atomic
    def delete(self, *, task: Task) -> None:
        task.delete()


# ------------------------------------------------------------------------------
# Job Services
# ------------------------------------------------------------------------------


class JobTypeService:
    def __init__(self, user=None):
        self.user = user

    def create(self, name: str, external_id: str = "", notes: str = "") -> JobType:
        job_type = JobType.objects.create(
            name=name, external_id=external_id, notes=notes
        )
        job_type.full_clean()
        job_type.save(user=self.user)

        return job_type

    def update(self, job_type: JobType, data: dict) -> JobType:
        fields = [
            "name",
            "external_id",
            "notes",
        ]

        job_type, _ = model_update(instance=job_type, fields=fields, data=data, user=self.user)

        return job_type

    def delete(self, job_type: JobType) -> None:
        job_type.delete()


class JobService:
    def __init__(self, user=None):
        self.user = user

    @transaction.atomic
    def create(
        self,
        name: str,
        due_date: datetime,
        job_type: JobType,
        customer: str = "",
        description: str = "",
        external_id: str = "",
        notes: str = "",
        priority: int = None,
    ) -> Job:
        job = Job.objects.create(
            name=name,
            due_date=due_date,
            job_type=job_type,
            customer=customer,
            external_id=external_id,
            notes=notes,
            description=description,
        )

        job.full_clean()
        job.save(user=self.user)

        job.update_priority(priority)

        return job

    @transaction.atomic
    def update(self, job: Job, data: dict) -> Job:
        fields = [
            "name",
            "due_date",
            "job_type",
            "customer",
            "description",
            "external_id",
            "notes",
            "dependencies",
        ]

        job, _ = model_update(instance=job, fields=fields, data=data, user=self.user)

        # update job priority
        if data.get("priority", None):
            job.update_priority(data["priority"])

        return job

    @transaction.atomic
    def delete(self, job: Job) -> None:
        job.delete()


# ------------------------------------------------------------------------------
# Dependency Services
# ------------------------------------------------------------------------------


class DependencyTypeService:
    def __init__(self, user=None):
        self.user = user

    def create(self, name: str, external_id: str = "", notes: str = "") -> DependencyType:
        dependency_type = DependencyType.objects.create(
            name=name, external_id=external_id, notes=notes
        )
        dependency_type.full_clean()
        dependency_type.save(user=self.user)

        return dependency_type

    def update(self, dependency_type: DependencyType, data: dict) -> DependencyType:
        fields = [
            "name",
            "external_id",
            "notes",
        ]

        dependency_type, _ = model_update(
            instance=dependency_type, fields=fields, data=data, user=self.user,
        )

        return dependency_type

    def delete(self, dependency_type: DependencyType) -> None:
        dependency_type.delete()


class DependencyService:
    def __init__(self, user=None):
        self.user = user

    @transaction.atomic
    def create(
        self,
        *,
        name: str,
        dependency_type: DependencyType,
        expected_close_datetime: datetime = None,
        notes: str = "",
        external_id: str = "",
        tasks: list[Task] = None,
        jobs: list[Job] = None,
    ) -> Dependency:
        dependency = Dependency.objects.create(
            name=name,
            dependency_type=dependency_type,
            expected_close_datetime=expected_close_datetime,
            notes=notes,
            external_id=external_id,
        )

        dependency.full_clean()
        dependency.save(user=self.user)

        if tasks:
            dependency.tasks.set(tasks)

        if jobs:
            dependency.jobs.set(jobs)

        return dependency

    @transaction.atomic
    def update(self, *, instance: Dependency, data: dict) -> Dependency:
        fields = [
            "name",
            "dependency_type",
            "expected_close_datetime",
            "notes",
            "external_id",
            "tasks",
            "jobs",
        ]

        dependency, _ = model_update(instance=instance, fields=fields, data=data, user=self.user)

        return dependency

    @transaction.atomic
    def delete(self, instance: Dependency) -> None:
        instance.delete()
