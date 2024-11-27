from api.permission_checker import AbstractPermissionService
from common.services import model_update
from common.utils import get_object
from django.core.exceptions import PermissionDenied
from django.db import transaction

from job_manager.models import (
    Dependency,
    Item,
    Job,
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
            assignment_constraint_dict.pop("task", None)
            assignment_constraint_dict.pop("id", None)
            assignment_constraint_dict.pop("DELETE", None)

            # get custom fields from assignment constraint
            constraint_custom_fields = assignment_constraint_dict.pop(
                "custom_fields", {}
            )

            self.assignment_constraint_service.create(
                task=task,
                **assignment_constraint_dict,
                custom_fields=constraint_custom_fields,
            )

        if dependencies:
            task.dependencies.set(dependencies)

        if predecessors:
            task.predecessors.set(predecessors)

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

        # delete the assignment constraints if Delete is True
        constraints_to_delete = (
            assignment_constraints[0].pop("DELETE", False)
            if assignment_constraints
            else False
        )

        if constraints_to_delete:
            # delete the assignment constraint
            constraints_instance = AssignmentConstraint.objects.filter(
                task=assignment_constraints[0]["task"]
            )
            if constraints_instance.exists():
                self.assignment_constraint_service.delete(
                    instance=constraints_instance.first()
                )

        if assignment_constraints and not constraints_to_delete:
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
