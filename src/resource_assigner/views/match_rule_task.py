from common.utils.views import add_notification_headers
from django.http import HttpResponse
from job_manager.models import JobStatusChoices, Task, TaskStatusChoices

# Create your views here.
from django_q.tasks import async_task

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

        # TODO:
        # store background task id and sync it with frontend
        background_task_id = async_task(
            "resource_assigner.utils.get_matching_assignment_rules_with_tasks"
        )

        response = HttpResponse(status=200)
        add_notification_headers(
            response,
            "The task has been started. You will be notified when it's done.",
            "success",
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
