from api.permission_checker import AbstractPermissionService

# validation error
from django.db import transaction
from job_manager.models.task import Task

from microbatching.models.microbatch_flow import MicrobatchFlow


class MicrobatchSchedulerService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)
        
    def update_predecessors(task, predecessor_list):
        """Update the predecessors of a task into its
        counterparts from the parent task's predecessors.
        """
        pass

    def update_parent_task(parent_task, subtasks):
        """Update the start_date and end_date of parent tasks
        based on subtask schedules.
        """
        pass

    @staticmethod
    def create_microbatch_subtasks(flow_tasks):
        """Create microbatch subtasks."""

        microbatched_tasks = []

        for flow_task in flow_tasks:
            batch_size = flow_task.microbatch_task_flow.microbatch_flow.batch_size
            task = flow_task.task
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
                task_group[task.id].append(subtask)

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
            
            microbatched_tasks.append(task_group)

        return microbatched_tasks

    @transaction.atomic
    def run(self):
        """Run the microbatch scheduler service."""
        try:
            # for flow in MicrobatchFlow.objects.order_by("order"):
            flow = MicrobatchFlow.objects.order_by("order").first()
            for task_flow in flow.task_flows.all():
                # tasks = [flow_task.task for flow_task in task_flow.flow_tasks.all()]
                if task_flow.flow_tasks.count() > 0:
                    self.create_microbatch_subtasks(task_flow.flow_tasks.all())

            # self.update_predecessors()
            # self.update_parent_task()
        except Exception as e:
            raise e



