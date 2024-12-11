from common.utils.views import add_notification_headers
from django.http import HttpResponse
from job_manager.models import JobStatusChoices, Task, TaskStatusChoices

# Create your views here.
from resource_assigner.utils import get_matching_assignment_rules_with_tasks

# ------------------------------------------------------------------------------
# Matching Rule API
# ------------------------------------------------------------------------------


def match_rules_with_tasks(request):
    """
    Match rules with tasks.
    """
    try:
        tasks = Task.objects.filter(
            task_status=TaskStatusChoices.NOT_STARTED,
            job__job_status__in=[
                JobStatusChoices.IN_PROGRESS,
                JobStatusChoices.NOT_PLANNED,
            ],
        )

        if tasks.count() == 0:
            raise Exception("Tasks not found!")

        result = get_matching_assignment_rules_with_tasks()

        response = HttpResponse(status=204)
        add_notification_headers(
            response,
            result["message"],
            result["status"],
        )
        return response
    except Exception as e:
        response = HttpResponse(status=500)
        add_notification_headers(
            response,
            str(e),
            "error",
        )
        return response
