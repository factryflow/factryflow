from django.http import JsonResponse
from django.views import View
from job_manager.services import JobGanttChartService, ResourceGanttChartService


class JobGanttAPIView(View):
    def get(self, request):
        """Use JobGanttChartService to map jobs to
        gantt chart data and return as JSON.
        """
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 50))

        service = JobGanttChartService(user=request.user)
        gantt_data = service.map_jobs_to_gantt(page=page, page_size=page_size)

        return JsonResponse(gantt_data, status=200, safe=False)


class ResourceGanttAPIView(View):
    def get(self, request):
        """Use ResourceGanttChartService to map resources to
        gantt chart data and return as JSON.
        """
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 50))

        service = ResourceGanttChartService(user=request.user)
        gantt_data = service.map_resources_to_gantt(page=page, page_size=page_size)

        return JsonResponse(gantt_data, status=200, safe=False)
