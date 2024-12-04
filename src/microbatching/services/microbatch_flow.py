from api.permission_checker import AbstractPermissionService
from common.services import model_update

# validation error
from django.core.exceptions import PermissionDenied
from django.db import transaction
from job_manager.models.task import Task
from resource_assigner.models import AssignmentConstraint, TaskRuleAssignment

from microbatching.models.microbatch_flow import MicrobatchFlow
from microbatching.models.microbatch_rule import MicrobatchRule


class MicrobatchFlowService:
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        name: str,
        description: str,
        start_rule: MicrobatchRule,
        end_rule: MicrobatchRule,
        min_flow_length: int,
        max_flow_length: int,
        batch_size: int,
        custom_fields: dict = None,
    ) -> MicrobatchFlow:
        # check permissions for create microbatch flow
        if not self.permission_service.check_for_permission("add_microbatchflow"):
            raise PermissionDenied()

        instance = MicrobatchFlow.objects.create(
            name=name,
            description=description,
            start_rule=start_rule,
            end_rule=end_rule,
            min_flow_length=min_flow_length,
            max_flow_length=max_flow_length,
            batch_size=batch_size,
            custom_fields=custom_fields,
        )

        instance.full_clean()
        instance.save(user=self.user)

        return instance

    @transaction.atomic
    def update(self, instance: MicrobatchFlow, data: dict) -> MicrobatchFlow:
        # check permissions for update microbatch rule
        if not self.permission_service.check_for_permission("change_microbatchflow"):
            raise PermissionDenied()

        fields = [
            "name",
            "description",
            "start_rule",
            "end_rule",
            "min_flow_length",
            "max_flow_length",
            "batch_size",
            "custom_fields",
        ]
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return instance

    @transaction.atomic
    def delete(self, instance: MicrobatchFlow) -> None:
        # check permissions for delete microbatch rule
        if not self.permission_service.check_for_permission("delete_microbatchflow"):
            raise PermissionDenied()

        instance.delete()
        return True

    @staticmethod
    def create_microbatch_subtasks(flow_tasks):
        """Create microbatch subtasks."""

        microbatched_tasks = []
        predecessor_group = None

        for flow_task in flow_tasks:
            batch_size = flow_task.microbatch_task_flow.microbatch_flow.batch_size
            task = flow_task.task

            if task.sub_tasks.exists():  # If task has subtasks, which means it's already been microbatched, skip.
                continue

            batch_count = int(task.quantity / batch_size)
            batch_remainder = task.quantity % batch_size

            task_group = {task.id: []}

            for i in range(batch_count):
                subtask = Task.objects.create(
                    name=f"{task.name}-{i + 1}",
                    item=task.item,
                    task_type=task.task_type,
                    job=task.job,
                    work_center=task.work_center,
                    run_time_per_unit=task.run_time_per_unit,
                    setup_time=task.setup_time,
                    teardown_time=task.teardown_time,
                    quantity=batch_size,
                    parent=task,
                    duration=task.run_time_per_unit * batch_size,
                )

                if (
                    task.taskruleassignment_set.exists()
                ):  # Create AssignmentRule for subtasks
                    if task.taskruleassignment_set.filter(is_applied=True).exists():
                        assignment_rule = (
                            task.taskruleassignment_set.filter(is_applied=True)
                            .first()
                            .assigment_rule
                        )
                    else:
                        assignment_rule = (
                            task.taskruleassignment_set.first().assigment_rule
                        )

                    TaskRuleAssignment.objects.create(
                        task=subtask, assigment_rule=assignment_rule
                    )

                if hasattr(
                    task, "assignmentconstraint"
                ):  # Create AssignmentConstraint for subtasks
                    parent_constraint = task.assignmentconstraint
                    assignment_constraint = AssignmentConstraint.objects.create(
                        task=subtask,
                        assignment_rule=parent_constraint.assignment_rule,
                        resource_group=parent_constraint.resource_group,
                        resource_count=parent_constraint.resource_count,
                        use_all_resources=parent_constraint.use_all_resources,
                    )
                    assignment_constraint.resources.set(
                        parent_constraint.resources.all()
                    )

                if predecessor_group:
                    try:  # Set subtask predecessors to their equivalent subtasks in the parent task's predecessor
                        subtask.predecessors.set([predecessor_group[i]])
                    except IndexError:
                        subtask.predecessors.clear()

                task_group[task.id].append(subtask)

            if batch_remainder > 0:
                remainder_subtask = Task.objects.create(
                    name=f"{task.name}-{batch_count + 1}",
                    item=task.item,
                    task_type=task.task_type,
                    job=task.job,
                    work_center=task.work_center,
                    run_time_per_unit=task.run_time_per_unit,
                    setup_time=task.setup_time,
                    teardown_time=task.teardown_time,
                    quantity=batch_remainder,
                    parent=task,
                    duration=task.run_time_per_unit * batch_remainder,
                )
                task_group[task.id].append(remainder_subtask)
                if predecessor_group:
                    try:  # Set subtask predecessors for remainder subtasks
                        remainder_subtask.predecessors.set(
                            [predecessor_group[batch_count]]
                        )
                    except IndexError:
                        remainder_subtask.predecessors.clear()

            microbatched_tasks.append(task_group)
            predecessor_group = [task for task in task_group[task.id]]

            # Set predecessors for next tasks with no subtasks
            successor_tasks = task.successors.filter(sub_tasks__isnull=True)
            if successor_tasks.exists():
                for successor_task in successor_tasks:
                    successor_task.predecessors.set(predecessor_group)

        return microbatched_tasks
