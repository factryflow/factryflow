from datetime import datetime

from api.permission_checker import AbstractPermissionService
from common.services import model_update
from common.utils import get_object
from django.core.exceptions import PermissionDenied
from django.db import transaction
from resource_assigner.models import TaskResourceAssigment
from resource_manager.models import Resource

from job_manager.models import (
    Dependency,
    DependencyType,
    Item,
    Job,
    JobStatusChoices,
    JobType,
    Task,
    TaskType,
    WorkCenter,
)

from resource_assigner.models import AssignmentConstraint
from resource_assigner.services import AssignmentConstraintService

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

        self.assignment_constraint_service = AssignmentConstraintService(user=user)

    def _create_or_update_constraints(
        self, assignment_constraints: list[dict], instance: Task
    ):
        # Create or update assignment constraints
        for assignment_constraint_dict in assignment_constraints:
            assignment_constraint_id = (
                assignment_constraint_dict.get("id").id
                if assignment_constraint_dict.get("id")
                else None
            )
            assignment_constraint_instance = get_object(
                model_or_queryset=AssignmentConstraint, id=assignment_constraint_id
            )
            if assignment_constraint_instance:
                self.assignment_constraint_service.update(
                    instance=assignment_constraint_instance,
                    data=assignment_constraint_dict,
                )
            else:
                assignment_constraint_dict.pop("task", instance)
                assignment_constraint_dict.pop("id", None)

                self.assignment_constraint_service.create(
                    task=instance,
                    **assignment_constraint_dict,
                )

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
        constraints: list[dict] = [],
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

        # Create assignment constraints
        for assignment_constraint_dict in constraints:
            # delete assignment rule object as it already been created
            assignment_constraint_dict.pop("task", task)
            assignment_constraint_dict.pop("id", None)

            self.assignment_constraint_service.create(
                task=task,
                **assignment_constraint_dict,
                custom_fields=custom_fields,
            )

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

        # update assignment constraints
        assignment_constraints = data.get("constraints", [])

        if assignment_constraints:
            # create or update assignment constraints
            self._create_or_update_constraints(
                assignment_constraints=assignment_constraints, instance=instance
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

    @transaction.atomic
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

    @transaction.atomic
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

    @transaction.atomic
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

    @transaction.atomic
    def delete(self, instance: Item) -> None:
        # check for permission to delete item
        if not self.permission_service.check_for_permission("delete_item"):
            raise PermissionDenied()

        instance.delete()
        return True


class JobGanttChartService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def map_jobs_to_gantt(self) -> list:
        # check for permission to view job gantt chart
        if not self.user.is_authenticated:
            raise PermissionDenied()

        job_data = []
        jobs = Job.objects.prefetch_related("tasks").order_by("priority")

        gantt_pid = 1

        for job in jobs:
            if job.tasks.count() > 0:
                job_pid = gantt_pid
                job_data.append(
                    {
                        "pID": job_pid,
                        "pName": job.name,
                        "pStart": "",
                        "pEnd": "",
                        "pClass": "gtaskblue",
                        "pLink": "",
                        "pMile": 0,
                        "pRes": "",
                        "pComp": 0,
                        "pGroup": 1,
                        "pParent": 0,
                        "pOpen": 1,
                        "pDepend": "",
                        "pCaption": "",
                        "pNotes": "",
                        "pPlanStart": job.planned_start_datetime,
                        "pPlanEnd": job.planned_end_datetime,
                    }
                )

                gantt_pid += 1

                for task in job.tasks.all():
                    if hasattr(task, "taskresourceassigment"):
                        assignment = task.taskresourceassigment
                        if assignment.resources:
                            resource_name = ", ".join(
                                [
                                    resource.name
                                    for resource in assignment.resources.all()
                                ]
                            )
                    else:
                        resource_name = ""

                    job_data.append(
                        {
                            "pID": gantt_pid,
                            "pName": task.name,
                            "pStart": "",
                            "pEnd": "",
                            "pClass": "gtaskblue",
                            "pLink": "",
                            "pMile": 0,
                            "pRes": resource_name,
                            "pComp": 0,
                            "pGroup": 0,
                            "pParent": job_pid,
                            "pOpen": 1,
                            "pDepend": list(
                                task.predecessors.values_list("id", flat=True)
                            ),
                            "pNotes": task.notes,
                            "priority": job.priority,
                            "pCaption": "",
                            "pPlanStart": task.planned_start_datetime,
                            "pPlanEnd": task.planned_end_datetime,
                        }
                    )

                    gantt_pid += 1

        return job_data


class ResourceGanttChartService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def map_resources_to_gantt(self) -> list:
        # check for permission to view job gantt chart
        if not self.user.is_authenticated:
            raise PermissionDenied()

        chart_data = []
        gantt_pid = 1  # Counter for object ID in Gantt chart

        resources = Resource.objects.all()

        # Get all TaskResourceAssigment and group by resources
        for resource in resources:
            # Get all TaskResourceAssigment for each resource
            task_ids = TaskResourceAssigment.objects.filter(
                resources__id__contains=resource.id
            ).values_list("task_id", flat=True)

            resource_pid = gantt_pid

            chart_data.append(
                {
                    "pID": resource_pid,
                    "pName": resource.name,
                    "pStart": "",
                    "pEnd": "",
                    "pClass": "gtaskblue",
                    "pLink": "",
                    "pMile": 0,
                    "pRes": "",
                    "pComp": 0,
                    "pGroup": 1,
                    "pParent": 0,
                    "pOpen": 1,
                    "pDepend": "",
                    "pCaption": "",
                    "pNotes": "",
                }
            )

            gantt_pid += 1
            resource_jobs = Job.objects.none()

            if task_ids:
                for task_id in (
                    task_ids
                ):  # Get all jobs for each resource based on the assigned tasks
                    resource_jobs = resource_jobs | Job.objects.filter(
                        tasks__id__contains=task_id
                    )

            for job in resource_jobs.distinct():
                job_pid = gantt_pid
                chart_data.append(
                    {
                        "pID": job_pid,
                        "pName": job.name,
                        "pStart": "",
                        "pEnd": "",
                        "pClass": "gtaskblue",
                        "pLink": "",
                        "pMile": 0,
                        "pRes": "",
                        "pComp": 0,
                        "pGroup": 1,
                        "pOpen": 1,
                        "pParent": resource_pid,
                        "pDepend": "",
                        "pCaption": "",
                        "pNotes": "",
                        "pPlanStart": job.planned_start_datetime,
                        "pPlanEnd": job.planned_end_datetime,
                    }
                )

                gantt_pid += 1

                for task in job.tasks.filter(id__in=task_ids):
                    if hasattr(task, "taskresourceassigment"):
                        assignment = task.taskresourceassigment
                        if assignment.resources:
                            resource_name = ", ".join(
                                [
                                    resource.name
                                    for resource in assignment.resources.all()
                                ]
                            )
                    else:
                        resource_name = ""

                    chart_data.append(
                        {
                            "pID": gantt_pid,
                            "pName": task.name,
                            "pStart": "",
                            "pEnd": "",
                            "pClass": "gtaskblue",
                            "pLink": "",
                            "pMile": 0,
                            "pRes": resource_name,
                            "pComp": 0,
                            "pGroup": 0,
                            "pParent": job_pid,
                            "pOpen": 1,
                            "pDepend": list(
                                task.predecessors.values_list("id", flat=True)
                            ),
                            "pCaption": "",
                            "pNotes": "",
                            "pPlanStart": task.planned_start_datetime,
                            "pPlanEnd": task.planned_end_datetime,
                        }
                    )

                    gantt_pid += 1

        return chart_data
