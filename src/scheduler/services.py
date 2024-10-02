from datetime import datetime, time, timedelta, timezone

import numpy as np
from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from factryengine import Assignment, ResourceGroup, Scheduler
from factryengine import Resource as SchedulerResource
from factryengine import Task as SchedulerTask
from job_manager.models import Task
from resource_assigner.models import (
    AssignmentConstraint,
    TaskResourceAssigment,
    TaskRuleAssignment,
)
from resource_calendar.models import OperationalException, WeeklyShiftTemplate
from resource_manager.models import Resource

from .constants import DAY_IN_MINUTES, WEEK_IN_MINUTES
from .models import ResourceAllocations, ResourceIntervals, SchedulerRuns

# --------------------------------------------------------
# Resource Intervals Service
# --------------------------------------------------------


class ResourceIntervalsService(AbstractPermissionService):
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def get_all_resource_intervals(self):
        # get all resource intervals
        if not self.permission_service.check_for_permission("view_resourcentervals"):
            raise PermissionDenied(
                "You do not have permission to view resource intervals"
            )

        return ResourceIntervals.objects.all()

    def get_resource_intervals_by_id(
        self, interval_id=None, resource_id=None, task_id=None
    ):
        # Check permission
        if not self.permission_service.check_for_permission("view_resourcentervals"):
            raise PermissionDenied(
                "You do not have permission to view resource intervals"
            )

        filters = Q()
        if interval_id:
            filters &= Q(id=interval_id)
        if resource_id:
            filters &= Q(resource_id=resource_id)
        if task_id:
            filters &= Q(task_id=task_id)

        # Apply filters to the queryset
        queryset = ResourceIntervals.objects.filter(filters)

        return queryset

    @transaction.atomic
    def create(
        self,
        scheduler_run: SchedulerRuns,
        resource: Resource,
        task: Task,
        interval_start,
        interval_end,
    ):
        # check permissions
        if not self.permission_service.check_for_permission("add_resourceintervals"):
            raise PermissionDenied(
                "You do not have permission to add resource intervals"
            )

        resource_interval = ResourceIntervals.objects.create(
            run_id=scheduler_run,
            resource=resource,
            task=task,
            interval_start=interval_start,
            interval_end=interval_end,
        )

        resource_interval.full_clean()
        resource_interval.save()
        return resource_interval

    @transaction.atomic
    def update(self, instance: ResourceIntervals, data: dict):
        if not self.permission_service.check_for_permission("change_resourceintervals"):
            raise PermissionDenied(
                "You do not have permission to change resource intervals"
            )

        fields = ["run_id", "resource", "task", "interval_start", "interval_end"]
        resource_interval = model_update(
            instance=instance, data=data, fields=fields, user=self.user
        )

        return resource_interval

    @transaction.atomic
    def delete(self, instance: ResourceIntervals):
        if not self.permission_service.check_for_permission("delete_resourceintervals"):
            raise PermissionDenied(
                "You do not have permission to delete resource intervals"
            )

        instance.delete()
        return True


# --------------------------------------------------------
# Resource Allocations Service
# --------------------------------------------------------


class ResourceAllocationsService(AbstractPermissionService):
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def get_all_resource_allocations(self):
        # get all resource allocations
        if not self.permission_service.check_for_permission("view_resourceallocations"):
            raise PermissionDenied(
                "You do not have permission to view resource allocations"
            )

        return ResourceAllocations.objects.all()

    def get_resource_allocations_by_id(self, resource_id=None, task_id=None):
        # Check permission
        if not self.permission_service.check_for_permission("view_resourceallocations"):
            raise PermissionDenied(
                "You do not have permission to view resource allocations"
            )

        filters = Q()
        if resource_id:
            filters &= Q(resource_id=resource_id)
        if task_id:
            filters &= Q(task_id=task_id)

        # Apply filters to the queryset
        queryset = ResourceAllocations.objects.filter(filters)

        return queryset

    @transaction.atomic
    def create(
        self,
        scheduler_run: SchedulerRuns,
        resource: Resource,
        task: Task,
    ):
        # check permissions
        if not self.permission_service.check_for_permission("add_resourceallocations"):
            raise PermissionDenied(
                "You do not have permission to add resource allocations"
            )

        resource_allocation = ResourceAllocations.objects.create(
            run_id=scheduler_run,
            resource=resource,
            task=task,
        )

        resource_allocation.full_clean()
        resource_allocation.save()
        return resource_allocation

    @transaction.atomic
    def update(self, instance: ResourceAllocations, data: dict):
        if not self.permission_service.check_for_permission(
            "change_resourceallocations"
        ):
            raise PermissionDenied(
                "You do not have permission to change resource allocations"
            )

        fields = ["run_id", "resource", "task"]
        resource_allocation = model_update(
            instance=instance, data=data, fields=fields, user=self.user
        )

        return resource_allocation

    @transaction.atomic
    def delete(self, instance: ResourceAllocations):
        if not self.permission_service.check_for_permission(
            "delete_resourceallocations"
        ):
            raise PermissionDenied(
                "You do not have permission to delete resource allocations"
            )

        instance.delete()
        return True


# --------------------------------------------------------
# Scheduler Runs Service
# --------------------------------------------------------


class SchedulerRunsService(AbstractPermissionService):
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)
        self.scheduler_runs = SchedulerRuns

    def get_all_scheduler_runs(self):
        # get all scheduler runs
        if not self.permission_service.check_for_permission("view_schedulerruns"):
            raise PermissionDenied("You do not have permission to view scheduler runs")

        return self.scheduler_runs.objects.all()

    def get_scheduler_runs_by_id(self, run_id=None):
        # Check permission
        if not self.permission_service.check_for_permission("view_schedulerruns"):
            raise PermissionDenied("You do not have permission to view scheduler runs")

        filters = Q()
        if run_id:
            filters &= Q(id=run_id)

        # Apply filters to the queryset
        queryset = self.scheduler_runs.objects.filter(filters)

        return queryset

    @transaction.atomic
    def create(
        self,
        start_time,
        status,
        end_time=None,
        run_duration=None,
        details=None,
    ):
        # check permissions
        if not self.permission_service.check_for_permission("add_schedulerruns"):
            raise PermissionDenied("You do not have permission to add scheduler runs")

        scheduler_run = SchedulerRuns.objects.create(
            start_time=start_time,
            end_time=end_time,
            run_duration=run_duration,
            details=details,
            status=status,
        )

        scheduler_run.full_clean()
        scheduler_run.save()
        return scheduler_run

    @transaction.atomic
    def update(self, instance: SchedulerRuns, data: dict):
        if not self.permission_service.check_for_permission("change_schedulerruns"):
            raise PermissionDenied(
                "You do not have permission to change scheduler runs"
            )

        fields = ["start_time", "end_time", "run_duration", "details", "status"]
        scheduler_run = model_update(
            instance=instance, data=data, fields=fields, user=self.user
        )

        return scheduler_run

    @transaction.atomic
    def delete(self, instance: SchedulerRuns):
        if not self.permission_service.check_for_permission("delete_schedulerruns"):
            raise PermissionDenied(
                "You do not have permission to delete scheduler runs"
            )

        instance.delete()
        return True


# --------------------------------------------------------
# Scheduling Service
# --------------------------------------------------------


class SchedulingService:
    def __init__(
        self,
        horizon_weeks: int = 1,
        plan_start_date: datetime = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        ),
    ):
        self.plan_start_date = plan_start_date
        self.plan_start_weekday = (
            plan_start_date.weekday() if self.plan_start_date else None
        )
        self.plan_start_minutes = (
            None
            if self.plan_start_weekday is None
            else self.plan_start_weekday * DAY_IN_MINUTES
        )
        self.horizon_weeks = horizon_weeks if horizon_weeks else 20
        self.horizon_minutes = horizon_weeks * WEEK_IN_MINUTES
        self.weekly_shift_templates_windows_dict = (
            self._get_weekly_shift_template_windows_dict()
        )

    @transaction.atomic
    def run(self):
        scheduler_resources_dict = self._create_scheduler_resource_objects_dict()
        scheduler_tasks = self._create_scheduler_task_objects(scheduler_resources_dict)
        scheduler_logs = {"tasks_found": 0, "tasks_assigned": 0}
        log_messages = []

        if "error" in scheduler_tasks:
            return {"error": scheduler_tasks["error"]}

        scheduler = Scheduler(
            tasks=scheduler_tasks, resources=scheduler_resources_dict.values()
        )
        result = scheduler.schedule()
        scheduler_summary = result.summary().split("\n")
        log_messages.extend(scheduler_summary)

        # convert result to dataframe
        res_df = result.to_dataframe()

        # convert 'task_start' and task_end and 'resource_intervals': dict_values to time
        res_df["planned_task_start"] = res_df.apply(
            lambda scheduled_task: str(
                self._int_to_datetime(scheduled_task["task_start"])
            ),
            axis=1,
        )

        res_df["planned_task_end"] = res_df.apply(
            lambda scheduled_task: str(
                self._int_to_datetime(scheduled_task["task_end"])
            ),
            axis=1,
        )

        # Clear TaskResourceAssigment model before creating new ones
        TaskResourceAssigment.objects.all().delete()
        log_messages.append("TaskResourceAssigment model cleared.")

        # save to TaskResourceAssigment model
        task_resource_assignments = []

        scheduler_results = result.to_dict()
        scheduler_logs["tasks_found"] = len(scheduler_results)

        for task in scheduler_results:
            task_id = task["task_id"]
            task_obj = Task.objects.get(id=task_id)

            if not task.get("error_message") == "No solution found.":
                # Update task planned start and end datetime
                task_obj.planned_start_datetime = self._int_to_datetime(
                    int(task["task_start"])
                )
                task_obj.planned_end_datetime = self._int_to_datetime(
                    int(task["task_end"])
                )
                task_obj.save()
                scheduler_logs["tasks_assigned"] += 1
                log_messages.append(f"Task with ID: {task_id} schedule updated.")

                # Create TaskResourceAssigment object
                task_resource_assignment = TaskResourceAssigment(task_id=task_id)
                task_resource_assignment.save()
                log_messages.append(
                    f"TaskResourceAssigment {task_resource_assignment.id} created for Task with ID: {task_id}."
                )

                if task.get("assigned_resource_ids"):
                    resource_ids = task["assigned_resource_ids"]
                    resources = Resource.objects.filter(id__in=resource_ids)
                    task_resource_assignment.resources.set(resources)
                    log_messages.append(
                        f"TaskResourceAssigment {task_resource_assignment.id} assigned to resources: {resource_ids}."
                    )

                task_resource_assignments.append(task_resource_assignment)

                # Set Task Job planned start and end datetime
                if task_obj == Task.objects.filter(job=task_obj.job).earliest(
                    "planned_start_datetime"
                ):
                    task_obj.job.planned_start_datetime = (
                        task_obj.planned_start_datetime
                    )
                    task_obj.job.save()
                    log_messages.append(
                        f"Job with ID {task_obj.job.id} planned_start_datetime updated."
                    )

                if task_obj == Task.objects.filter(job=task_obj.job).latest(
                    "planned_end_datetime"
                ):
                    task_obj.job.planned_end_datetime = task_obj.planned_end_datetime
                    task_obj.job.save()
                    log_messages.append(
                        f"Job with ID {task_obj.job.id} planned_end_datetime updated."
                    )

        scheduler_logs["log_messages"] = log_messages
        return {"data": res_df.to_dict("records"), "logs": scheduler_logs}

    def _create_scheduler_task_objects(self, resources_dict: dict):
        tasks = Task.objects.filter(job__isnull=False)

        scheduler_tasks = []
        scheduler_assignments = []
        for task in tasks:
            scheduler_task_dict = {}

            # task details
            scheduler_task_dict["id"] = task.id
            scheduler_task_dict["duration"] = task.duration
            scheduler_task_dict["priority"] = task.job.priority
            scheduler_task_dict["quantity"] = task.quantity

            predecessor_ids = (
                [predecessor.id for predecessor in task.predecessors.all()]
                if task.predecessors
                else []
            )

            if len(predecessor_ids) > 0:
                scheduler_task_dict["predecessor_ids"] = (
                    predecessor_ids if len(predecessor_ids) > 0 else []
                )

            # get constraints related to task if there are any
            constraints = self._get_task_constraints(task)

            if len(constraints) > 0:
                # add constraints to dictionary
                scheduler_task_dict["constraints"] = constraints

            rule_assignment = TaskRuleAssignment.objects.filter(task=task).first()

            if rule_assignment and len(constraints) == 0:
                # check for assignments
                scheduler_group_list = []

                if hasattr(rule_assignment.assigment_rule, "assignmentconstraint"):
                    assignment_constraint = (
                        rule_assignment.assigment_rule.assignmentconstraint
                    )
                    resource_count = assignment_constraint.resource_count
                    scheduler_assignment = None

                    assigned_resources = (
                        assignment_constraint.resource_group.resources.all()
                        if assignment_constraint.resource_group
                        else assignment_constraint.resources.all()
                    )

                    group_resources = []
                    for resource in assigned_resources:
                        available_windows = (
                            self.weekly_shift_templates_windows_dict.get(
                                resource.weekly_shift_template.id, []
                            )
                        )
                        resource_data = SchedulerResource(
                            id=resource.id,
                            available_windows=available_windows,
                        )
                        group_resources.append(resource_data)

                    scheduler_resource_group = ResourceGroup(resources=group_resources)
                    scheduler_group_list.append(scheduler_resource_group)

                    if (
                        resource_count > 0
                        and not assignment_constraint.use_all_resources
                    ):
                        scheduler_assignment = Assignment(
                            resource_groups=[scheduler_resource_group],
                            resource_count=resource_count,
                        )

                    if assignment_constraint.use_all_resources:
                        scheduler_assignment = Assignment(
                            resource_groups=[scheduler_resource_group],
                            use_all_resources=assignment_constraint.use_all_resources,
                        )

                    # append all the scheduler assignment to the scheduler_assignments list
                    if scheduler_assignment:
                        scheduler_assignments.append(scheduler_assignment)

            # add assignments to scheduler task dictionary
            scheduler_task_dict["assignments"] = scheduler_assignments

            try:
                scheduler_task = SchedulerTask(**scheduler_task_dict)
                scheduler_tasks.append(scheduler_task)
            except Exception as e:
                return {"error": str(e)}

        return scheduler_tasks

    def _get_task_constraints(self, task):
        # get all resources from AssignmentConstraint model where task is equal to task
        constraints = []
        constraint_resource_tasks = AssignmentConstraint.objects.filter(
            task=task
        ).first()

        if constraint_resource_tasks:
            # if resources is not empty, get all resources from the resources field else get all resources from the resource_group field
            assigned_resources = (
                constraint_resource_tasks.resource_group.resources.all()
                if constraint_resource_tasks.resource_group
                else constraint_resource_tasks.resources.all()
            )

            for resource in assigned_resources:
                available_windows = self.weekly_shift_templates_windows_dict.get(
                    resource.weekly_shift_template.id, []
                )

                resource_data = SchedulerResource(
                    id=resource.id,
                    available_windows=available_windows,
                )

                constraints.append(resource_data)

        return constraints

    # Convert periods to time
    def _int_to_datetime(self, num):
        try:
            # Parse the start time string into a datetime object
            start_datetime = self.plan_start_date.replace(tzinfo=timezone.utc)

            # Add the number of minutes to the start datetime
            delta = timedelta(minutes=num)
            result_datetime = start_datetime + delta
            return result_datetime

        except Exception as e:
            print(str(e))

    def _get_task_assigned_resource_ids(self, task):
        resources = []
        resource_count = None

        # get all resource ids from TaskResourceAssigment model where task_id is equal to task.id
        task_resource_assignments = TaskResourceAssigment.objects.filter(
            task_id=task.id
        )
        for task_resource_assignment in task_resource_assignments:
            resources.append(task_resource_assignment.resource)

        if resources:
            resource_count = len(resources)

        resource_ids = [resource.id for resource in resources]

        return (resource_ids, resource_count)

    def _create_scheduler_resource_objects_dict(self):
        resources = Resource.objects.all()
        scheduler_resources = {}
        for resource in resources:
            available_windows = self.weekly_shift_templates_windows_dict.get(
                resource.weekly_shift_template.id, []
            )
            scheduler_resource = SchedulerResource(
                id=resource.id, available_windows=available_windows
            )
            scheduler_resources[resource.id] = scheduler_resource

        return scheduler_resources

    def _get_weekly_shift_template_windows_dict(self) -> dict:
        weekly_shift_templates = WeeklyShiftTemplate.objects.all()
        weekly_shift_template_windows_dict = {}
        for weekly_shift_template in weekly_shift_templates:
            weekly_shift_template_windows_dict[weekly_shift_template.id] = (
                self._weekly_shift_template_to_windows(weekly_shift_template)
            )
        return weekly_shift_template_windows_dict

    def _get_operational_exceptions(self, operational_exceptions: OperationalException):
        # convert operational exceptions to minutes
        exceptions = []
        for exception in operational_exceptions:
            start_minutes = self._datetime_to_minutes(exception.start_datetime)
            end_minutes = self._datetime_to_minutes(exception.end_datetime)
            exceptions.append((start_minutes, end_minutes))

        return exceptions

    def _weekly_shift_template_to_windows(
        self, weekly_shift_template: WeeklyShiftTemplate
    ):
        details = weekly_shift_template.weekly_shift_template_details.all()

        weekly_windows = [self._detail_to_minutes(detail) for detail in details]
        windows = self._calculate_windows(weekly_windows)

        return windows

    def _calculate_windows(self, weekly_windows: list):
        weekly_windows = np.array(weekly_windows)
        # Create an increment array
        increment = WEEK_IN_MINUTES * np.arange(self.horizon_weeks + 1).reshape(
            -1, 1, 1
        )

        # Repeat the pattern and add the increment
        windows = weekly_windows + increment

        # subtract plan start
        windows = windows - self.plan_start_minutes

        # filter
        windows = windows[(windows >= 0) & (windows <= self.horizon_minutes)]

        return windows.reshape(-1, 2)

    def _detail_to_minutes(self, detail):
        start_time_minutes = self._time_to_minutes(detail.start_time)
        end_time_minutes = self._time_to_minutes(detail.end_time)
        week_offset_minutes = detail.get_day_of_week_number() * DAY_IN_MINUTES

        return (
            start_time_minutes + week_offset_minutes,
            end_time_minutes + week_offset_minutes,
        )

    def _time_to_minutes(self, time: time):
        return time.hour * 60 + time.minute

    def _minutes_to_time(self, minutes):
        # the day of the week offset
        days = minutes // (24 * 60)
        minutes %= 24 * 60

        # hours and minutes
        hours = minutes // 60
        minutes %= 60
        time_delta = timedelta(days=days)

        # Create a time object
        time_obj = (
            datetime.combine(datetime.min, time(hour=hours, minute=minutes))
            + time_delta
        ).time()

        return time_obj
