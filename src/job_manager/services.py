from datetime import datetime

from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied
from django.db import transaction

from job_manager.models import (
    Dependency,
    DependencyType,
    Job,
    JobStatusChoices,
    JobType,
    Task,
    TaskType,
    WorkCenter,
    Item,
)

# ------------------------------------------------------------------------------
# WorkCenter Services
# ------------------------------------------------------------------------------


class WorkCenterService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self,
        name: str,
        notes: str = "",
        external_id: str = "",
        custom_fields: dict = None,
    ) -> WorkCenter:
        # check for permission to create work center
        if not self.permission_service.check_for_permission("add_workcenter"):
            raise PermissionDenied()

        work_center = WorkCenter.objects.create(
            name=name, notes=notes, external_id=external_id, custom_fields=custom_fields
        )
        work_center.full_clean()
        work_center.save(user=self.user)

        return work_center

    def update(self, work_center: WorkCenter, data: dict) -> WorkCenter:
        # check for permission to update work center
        if not self.permission_service.check_for_permission("change_workcenter"):
            raise PermissionDenied()

        fields = ["name", "notes", "external_id", "custom_fields"]

        work_center, _ = model_update(
            instance=work_center, fields=fields, data=data, user=self.user
        )

        return work_center

    def delete(self, work_center: WorkCenter) -> None:
        # check for permission to delete work center
        if not self.permission_service.check_for_permission("delete_workcenter"):
            raise PermissionDenied()

        work_center.delete()
        return True


# ------------------------------------------------------------------------------
# Task Type Services
# ------------------------------------------------------------------------------


class TaskTypeService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self, name: str, notes: str, external_id: str = "", custom_fields: dict = None
    ) -> TaskType:
        # check for permission to create task type
        if not self.permission_service.check_for_permission("add_tasktype"):
            raise PermissionDenied()

        task_type = TaskType.objects.create(
            name=name, notes=notes, external_id=external_id, custom_fields=custom_fields
        )
        task_type.full_clean()
        task_type.save(user=self.user)

        return task_type

    def update(self, task_type: TaskType, data: dict) -> TaskType:
        # check for permission to update task type
        if not self.permission_service.check_for_permission("change_tasktype"):
            raise PermissionDenied()

        fields = ["name", "notes", "external_id", "custom_fields"]

        task_type, _ = model_update(
            instance=task_type, fields=fields, data=data, user=self.user
        )
        return task_type

    def delete(self, task_type: TaskType) -> None:
        # check for permission to delete task type
        if not self.permission_service.check_for_permission("delete_tasktype"):
            raise PermissionDenied()

        task_type.delete()
        return True


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
        name: str,
        quantity: int,
        task_type: TaskType,
        run_time_per_unit: int = 1,
        setup_time: int = 0,
        teardown_time: int = 0,
        duration: int = 0,
        external_id: str = "",
        notes="",
        item: Item = None,
        task_status: str = "NS",
        work_center: WorkCenter = None,
        job: Job = None,
        dependencies: list[Dependency] = None,
        predecessors: list[Task] = None,
        successors: list[Task] = None,
        custom_fields: dict = None,
    ) -> Task:
        # check for permission to create task
        if not self.permission_service.check_for_permission("add_task"):
            raise PermissionDenied()

        task = Task.objects.create(
            name=name,
            external_id=external_id,
            run_time_per_unit=run_time_per_unit,
            notes=notes,
            setup_time=setup_time,
            item=item,
            duration=duration,
            task_status=task_status,
            teardown_time=teardown_time,
            quantity=quantity,
            task_type=task_type,
            work_center=work_center,
            job=job,
            custom_fields=custom_fields,
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
    def update(self, instance: Task, data: dict) -> Task:
        # check for permission to update task
        if not self.permission_service.check_for_permission("change_task"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "notes",
            "setup_time",
            "teardown_time",
            "duration",
            "run_time_per_unit",
            "quantity",
            "item",
            "task_type",
            "work_center",
            "job",
            "dependencies",
            "predecessors",
            "successors",
            "custom_fields",
        ]

        task, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return task

    @transaction.atomic
    def delete(self, task: Task) -> None:
        # check for permission to delete task
        if not self.permission_service.check_for_permission("delete_task"):
            raise PermissionDenied()

        task.delete()
        return True


# ------------------------------------------------------------------------------
# Job Services
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

    def delete(self, job_type: JobType) -> None:
        # check for permission to delete job type
        if not self.permission_service.check_for_permission("delete_jobtype"):
            raise PermissionDenied()

        job_type.delete()
        return True


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


# ------------------------------------------------------------------------------
# Dependency Services
# ------------------------------------------------------------------------------


class DependencyTypeService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self,
        name: str,
        external_id: str = "",
        notes: str = "",
        custom_fields: dict = None,
    ) -> DependencyType:
        # check for permission to create dependency type
        if not self.permission_service.check_for_permission("add_dependencytype"):
            raise PermissionDenied()

        dependency_type = DependencyType.objects.create(
            name=name, external_id=external_id, notes=notes, custom_fields=custom_fields
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
            "custom_fields",
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
        return True


class DependencyService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        name: str,
        dependency_type: DependencyType,
        dependency_status: str = "PD",
        expected_close_datetime: datetime = None,
        notes: str = "",
        external_id: str = "",
        custom_fields: dict = None,
    ) -> Dependency:
        # check for permission to create dependency
        if not self.permission_service.check_for_permission("add_dependency"):
            raise PermissionDenied()

        dependency = Dependency.objects.create(
            name=name,
            dependency_type=dependency_type,
            expected_close_datetime=expected_close_datetime,
            notes=notes,
            dependency_status=dependency_status,
            external_id=external_id,
            custom_fields=custom_fields,
        )

        dependency.full_clean()
        dependency.save(user=self.user)

        return dependency

    @transaction.atomic
    def update(self, instance: Dependency, data: dict) -> Dependency:
        # check for permission to update dependency
        if not self.permission_service.check_for_permission("change_dependency"):
            raise PermissionDenied()

        fields = [
            "name",
            "dependency_type",
            "dependency_status",
            "expected_close_datetime",
            "actual_close_datetime",
            "notes",
            "external_id",
            "custom_fields",
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
        return True


# ------------------------------------------------------------------------------
# Item Services
# ------------------------------------------------------------------------------


class ItemService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self,
        name: str,
        description: str = "",
        external_id: str = "",
        notes: str = "",
        custom_fields: dict = None,
    ) -> Item:
        # check for permission to create item
        if not self.permission_service.check_for_permission("add_item"):
            raise PermissionDenied()

        item = Item.objects.create(
            name=name,
            description=description,
            external_id=external_id,
            notes=notes,
            custom_fields=custom_fields,
        )
        item.full_clean()
        item.save(user=self.user)

        return item

    def update(self, instance: Item, data: dict) -> Item:
        # check for permission to update item
        if not self.permission_service.check_for_permission("change_item"):
            raise PermissionDenied()

        fields = [
            "name",
            "description",
            "external_id",
            "notes",
            "custom_fields",
        ]

        item, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return item

    def delete(self, instance: Item) -> None:
        # check for permission to delete item
        if not self.permission_service.check_for_permission("delete_item"):
            raise PermissionDenied()

        instance.delete()
        return True
