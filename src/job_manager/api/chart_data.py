from django.http import HttpResponse
from django.views import View
from job_manager.services import JobGanttChartService


class JobGanttAPIView(View):
    def get(self, request):
        """Use JobGanttChartService to map jobs to
        gantt chart data and return as JSON.
        """
        service = JobGanttChartService(user=request.user)
        gantt_data = service.map_jobs_to_gantt()

        return HttpResponse(gantt_data, status=200)
