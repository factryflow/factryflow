from django.http import JsonResponse
from django.views import View
from job_manager.services import JobGanttChartService, ResourceGanttChartService


class JobGanttAPIView(View):
    def get(self, request):
        """Use JobGanttChartService to map jobs to
        gantt chart data and return as JSON.
        """
        service = JobGanttChartService(user=request.user)
        gantt_data = service.map_jobs_to_gantt()

        return JsonResponse(gantt_data, status=200, safe=False)


class ResourceGanttAPIView(View):
    def get(self, request):
        """Use JobGanttChartService to map jobs to
        gantt chart data and return as JSON.
        """
        service = ResourceGanttChartService(user=request.user)
        gantt_data = service.map_resources_to_gantt()

        return JsonResponse(gantt_data, status=200, safe=False)
