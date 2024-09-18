from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from scheduler.models import SchedulerLog


class SchedulerLogsAPIView(View):
    def get(self, request, scheduler_run_id):
        """GET logs for a given scheduler run."""

        scheduler_log = get_object_or_404(
            SchedulerLog, scheduler_run_id=scheduler_run_id
        )

        return JsonResponse(scheduler_log.logs, status=200)
