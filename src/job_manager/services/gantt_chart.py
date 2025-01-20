from api.permission_checker import AbstractPermissionService
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
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

    def get_flattened_job_data(self, jobs):
        """Helper method to flatten jobs and tasks into a single list for pagination"""
        flattened_data = []
        pid = 1

        for job in jobs:
            if job.tasks.count() > 0:
                # Add job
                job_pid = pid
                flattened_data.append({
                    "type": "job",
                    "pid": job_pid,
                    "job": job,
                })
                pid += 1

                # Add tasks
                for task in job.tasks.all():
                    flattened_data.append({
                        "type": "task",
                        "pid": pid,
                        "task": task,
                        "parent_pid": job_pid,
                        "job": job,
                    })
                    pid += 1

        return flattened_data

    def map_jobs_to_gantt(self, page=1, page_size=50) -> dict:
        """Map jobs to gantt chart data with proper pagination"""
        if not self.user.is_authenticated:
            raise PermissionDenied()

        # Get all jobs with their tasks
        jobs = Job.objects.prefetch_related("tasks").order_by("priority")
        
        # Flatten jobs and tasks into a single list for pagination
        flattened_data = self.get_flattened_job_data(jobs)
        
        # Create paginator
        paginator = Paginator(flattened_data, page_size)
        current_page = paginator.get_page(page)
        
        # Convert paginated items to gantt format
        job_data = []
        for item in current_page:
            if item["type"] == "job":
                job_data.append({
                    "pID": item["pid"],
                    "pName": item["job"].name,
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
                    "pPlanStart": item["job"].planned_start_datetime,
                    "pPlanEnd": item["job"].planned_end_datetime,
                })
            else:  # task
                task = item["task"]
                resource_name = ""
                if hasattr(task, "taskresourceassigment"):
                    assignment = task.taskresourceassigment
                    if assignment.resources:
                        resource_name = ", ".join([
                            resource.name
                            for resource in assignment.resources.all()
                        ])

                job_data.append({
                    "pID": item["pid"],
                    "pName": task.name,
                    "pStart": "",
                    "pEnd": "",
                    "pClass": "gtaskblue",
                    "pLink": "",
                    "pMile": 0,
                    "pRes": resource_name,
                    "pComp": 0,
                    "pGroup": 0,
                    "pParent": item["parent_pid"],
                    "pOpen": 1,
                    "pDepend": list(task.predecessors.values_list("id", flat=True)),
                    "pNotes": task.notes,
                    "priority": item["job"].priority,
                    "pCaption": "",
                    "pPlanStart": task.planned_start_datetime,
                    "pPlanEnd": task.planned_end_datetime,
                })

        return {
            "data": job_data,
            "total_count": paginator.count,
            "page": page,
            "page_size": page_size,
            "items_in_page": len(job_data)
        }


# ------------------------------------------------------------------------------
# Resource Gantt Chart Service
# ------------------------------------------------------------------------------


class ResourceGanttChartService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def get_flattened_resource_data(self, resources):
        """Helper method to flatten resources, jobs and tasks into a single list for pagination"""
        flattened_data = []
        pid = 1

        for resource in resources:
            # Add resource
            resource_pid = pid
            flattened_data.append({
                "type": "resource",
                "pid": resource_pid,
                "resource": resource,
            })
            pid += 1

            # Get all tasks for this resource
            task_ids = TaskResourceAssigment.objects.filter(
                resources=resource
            ).values_list("task_id", flat=True)

            resource_jobs = Job.objects.none()
            if task_ids:
                for task_id in task_ids:
                    resource_jobs = resource_jobs | Job.objects.filter(
                        tasks__id__contains=task_id
                    )

            # Add jobs and their tasks
            for job in resource_jobs.distinct():
                job_pid = pid
                flattened_data.append({
                    "type": "job",
                    "pid": job_pid,
                    "job": job,
                    "parent_pid": resource_pid,
                })
                pid += 1

                # Add tasks
                for task in job.tasks.filter(id__in=task_ids):
                    flattened_data.append({
                        "type": "task",
                        "pid": pid,
                        "task": task,
                        "parent_pid": job_pid,
                        "job": job,
                    })
                    pid += 1

        return flattened_data

    def map_resources_to_gantt(self, page=1, page_size=50) -> dict:
        """Map resources to gantt chart data with proper pagination"""
        if not self.user.is_authenticated:
            raise PermissionDenied()

        # Get all resources
        resources = Resource.objects.all()
        
        # Flatten resources, jobs and tasks into a single list for pagination
        flattened_data = self.get_flattened_resource_data(resources)
        
        # Create paginator
        paginator = Paginator(flattened_data, page_size)
        current_page = paginator.get_page(page)
        
        # Convert paginated items to gantt format
        chart_data = []
        for item in current_page:
            if item["type"] == "resource":
                chart_data.append({
                    "pID": item["pid"],
                    "pName": item["resource"].name,
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
                })
            elif item["type"] == "job":
                chart_data.append({
                    "pID": item["pid"],
                    "pName": item["job"].name,
                    "pStart": "",
                    "pEnd": "",
                    "pClass": "gtaskblue",
                    "pLink": "",
                    "pMile": 0,
                    "pRes": "",
                    "pComp": 0,
                    "pGroup": 1,
                    "pOpen": 1,
                    "pParent": item["parent_pid"],
                    "pDepend": "",
                    "pCaption": "",
                    "pNotes": "",
                    "pPlanStart": item["job"].planned_start_datetime,
                    "pPlanEnd": item["job"].planned_end_datetime,
                })
            else:  # task
                task = item["task"]
                resource_name = ""
                if hasattr(task, "taskresourceassigment"):
                    assignment = task.taskresourceassigment
                    if assignment.resources:
                        resource_name = ", ".join([
                            resource.name
                            for resource in assignment.resources.all()
                        ])

                chart_data.append({
                    "pID": item["pid"],
                    "pName": task.name,
                    "pStart": "",
                    "pEnd": "",
                    "pClass": "gtaskblue",
                    "pLink": "",
                    "pMile": 0,
                    "pRes": resource_name,
                    "pComp": 0,
                    "pGroup": 0,
                    "pParent": item["parent_pid"],
                    "pOpen": 1,
                    "pDepend": list(task.predecessors.values_list("id", flat=True)),
                    "pCaption": "",
                    "pNotes": "",
                    "pPlanStart": task.planned_start_datetime,
                    "pPlanEnd": task.planned_end_datetime,
                })

        return {
            "data": chart_data,
            "total_count": paginator.count,
            "page": page,
            "page_size": page_size,
            "items_in_page": len(chart_data)
        }
