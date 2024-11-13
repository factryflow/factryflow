
from api.permission_checker import AbstractPermissionService
from django.db import transaction
from job_manager.models.task import Task
from job_manager.utils import (
    consolidate_job_datetimes,
    consolidate_parent_task_datetimes,
)
from resource_assigner.models import AssignmentConstraint, TaskRuleAssignment
from scheduler.services import SchedulingService

from microbatching.models.microbatch_flow import MicrobatchFlow


class MicrobatchSchedulerService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

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

                if task.taskruleassignment_set.exists():  # Create AssignmentRule for subtasks
                    if task.taskruleassignment_set.filter(is_applied=True).exists():
                        assignment_rule = task.taskruleassignment_set.filter(is_applied=True).first().assigment_rule
                    else:
                        assignment_rule = task.taskruleassignment_set.first().assigment_rule

                    TaskRuleAssignment.objects.create(
                        task=subtask,
                        assigment_rule=assignment_rule
                    )

                if hasattr(task, "assignmentconstraint"):  # Create AssignmentConstraint for subtasks
                    parent_constraint = task.assignmentconstraint
                    assignment_constraint = AssignmentConstraint.objects.create(
                        task=subtask,
                        assignment_rule=parent_constraint.assignment_rule,
                        resource_group=parent_constraint.resource_group,
                        resource_count=parent_constraint.resource_count,
                        use_all_resources=parent_constraint.use_all_resources
                    )
                    assignment_constraint.resources.set(parent_constraint.resources.all())

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
                        remainder_subtask.predecessors.set([predecessor_group[batch_count]])
                    except IndexError:
                        remainder_subtask.predecessors.clear()
            
            microbatched_tasks.append(task_group)
            predecessor_group = [task for task in task_group[task.id]]

        return microbatched_tasks

    @transaction.atomic
    def run(self):
        """Run the microbatch scheduler service."""
        try:
            microbatched_tasks = []

            for flow in MicrobatchFlow.objects.order_by("order"):  # Run microbatching for every MicrobatchFlow based on order.
                flow = MicrobatchFlow.objects.order_by("order").first()
                for task_flow in flow.task_flows.all():
                    if task_flow.flow_tasks.count() > 0:
                        microbatched_tasks = self.create_microbatch_subtasks(task_flow.flow_tasks.all())

            SchedulingService(horizon_weeks=5).run(selected_tasks=Task.objects.filter(parent__isnull=False))  # Run the scheduler for the microbatched subtasks

            consolidate_parent_task_datetimes()  # Updates the parent Task datetimes based on the Subtask start/end datetimes
            consolidate_job_datetimes()  # Updates the Job datetimes based on the new parent Task datetimes

            return microbatched_tasks
        except Exception as e:
            raise e



