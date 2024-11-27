from api.permission_checker import AbstractPermissionService
from django.core.exceptions import PermissionDenied
from resource_assigner.models import TaskResourceAssigment
from resource_manager.models import Resource

from job_manager.models import Job


# ------------------------------------------------------------------------------
# Job Gantt Chart Service
# ------------------------------------------------------------------------------


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
    

# ------------------------------------------------------------------------------
# Resource Gantt Chart Service
# ------------------------------------------------------------------------------


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
