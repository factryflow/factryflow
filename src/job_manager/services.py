from datetime import datetime

from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied
from django.db import transaction

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
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)


    def create(self, name: str, notes: str) -> WorkCenter:
        # check for permission to create work center
        if not self.permission_service.check_for_permission("add_workcenter"):
            raise PermissionDenied()

        work_center = WorkCenter.objects.create(name=name, notes=notes)
        work_center.full_clean()
        work_center.save(user=self.user)

        return work_center

    def update(self, work_center: WorkCenter, data: dict) -> WorkCenter:
        # check for permission to update work center
        if not self.permission_service.check_for_permission("change_workcenter"):
            raise PermissionDenied()

        fields = [
            "name",
            "notes",
        ]

        work_center, _ = model_update(
            instance=work_center, fields=fields, data=data, user=self.user
        )

        return work_center

    def delete(self, work_center: WorkCenter) -> None:
        # check for permission to delete work center
        if not self.permission_service.check_for_permission("delete_workcenter"):
            raise PermissionDenied()

        work_center.delete()


# ------------------------------------------------------------------------------
# Task Type Services
# ------------------------------------------------------------------------------


class TaskTypeService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(self, name: str) -> TaskType:
        # check for permission to create task type
        if not self.permission_service.check_for_permission("add_tasktype"):
            raise PermissionDenied()

        task_type = TaskType.objects.create(name=name)
        task_type.full_clean()
        task_type.save(user=self.user)

        return task_type

    def update(self, task_type: TaskType, data: dict) -> TaskType:
        # check for permission to update task type
        if not self.permission_service.check_for_permission("change_tasktype"):
            raise PermissionDenied()

        fields = [
            "name",
        ]

        task_type, _ = model_update(
            instance=task_type, fields=fields, data=data, user=self.user
        )
        return task_type

    def delete(self, task_type: TaskType) -> None:
        # check for permission to delete task type
        if not self.permission_service.check_for_permission("delete_tasktype"):
            raise PermissionDenied()

        task_type.delete()


# ------------------------------------------------------------------------------
# Task Services
# ------------------------------------------------------------------------------


class TaskService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

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
        # check for permission to create task
        if not self.permission_service.check_for_permission("add_task"):
            raise PermissionDenied()

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
        # check for permission to update task
        if not self.permission_service.check_for_permission("change_task"):
            raise PermissionDenied()

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

        task, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return task

    @transaction.atomic
    def delete(self, *, task: Task) -> None:
        # check for permission to delete task
        if not self.permission_service.check_for_permission("delete_task"):
            raise PermissionDenied()

        task.delete()


# ------------------------------------------------------------------------------
# Job Services
# ------------------------------------------------------------------------------


class JobTypeService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(self, name: str, external_id: str = "", notes: str = "") -> JobType:
        # check for permission to create job type
        if not self.permission_service.check_for_permission("add_jobtype"):
            raise PermissionDenied()

        job_type = JobType.objects.create(
            name=name, external_id=external_id, notes=notes
        )
        job_type.full_clean()
        job_type.save(user=self.user)

        return job_type

    def update(self, job_type: JobType, data: dict) -> JobType:
        # check for permission to update job type
        if not self.permission_service.check_for_permission("change_jobtype"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "notes",
        ]

        job_type, _ = model_update(
            instance=job_type, fields=fields, data=data, user=self.user
        )

        return job_type

    def delete(self, job_type: JobType) -> None:
        # check for permission to delete job type
        if not self.permission_service.check_for_permission("delete_jobtype"):
            raise PermissionDenied()

        job_type.delete()


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
        customer: str = "",
        description: str = "",
        external_id: str = "",
        notes: str = "",
        priority: int = None,
    ) -> Job:
        # check for permission to create job
        if not self.permission_service.check_for_permission("add_job"):
            raise PermissionDenied()

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


# ------------------------------------------------------------------------------
# Dependency Services
# ------------------------------------------------------------------------------


class DependencyTypeService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self, name: str, external_id: str = "", notes: str = ""
    ) -> DependencyType:
        # check for permission to create dependency type
        if not self.permission_service.check_for_permission("add_dependencytype"):
            raise PermissionDenied()

        dependency_type = DependencyType.objects.create(
            name=name, external_id=external_id, notes=notes
        )
        dependency_type.full_clean()
        dependency_type.save(user=self.user)

        return dependency_type

    def update(self, dependency_type: DependencyType, data: dict) -> DependencyType:
        # check for permission to update dependency type
        if not self.permission_service.check_for_permission("change_dependencytype"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "notes",
        ]

        dependency_type, _ = model_update(
            instance=dependency_type,
            fields=fields,
            data=data,
            user=self.user,
        )

        return dependency_type

    def delete(self, dependency_type: DependencyType) -> None:
        # check for permission to delete dependency type
        if not self.permission_service.check_for_permission("delete_dependencytype"):
            raise PermissionDenied()

        dependency_type.delete()


class DependencyService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

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
        # check for permission to create dependency
        if not self.permission_service.check_for_permission("add_dependency"):
            raise PermissionDenied()

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
        # check for permission to update dependency
        if not self.permission_service.check_for_permission("change_dependency"):
            raise PermissionDenied()

        fields = [
            "name",
            "dependency_type",
            "expected_close_datetime",
            "notes",
            "external_id",
            "tasks",
            "jobs",
        ]

        dependency, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return dependency

    @transaction.atomic
    def delete(self, instance: Dependency) -> None:
        # check for permission to delete dependency
        if not self.permission_service.check_for_permission("delete_dependency"):
            raise PermissionDenied()

        instance.delete()
