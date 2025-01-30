from common.utils.ordered_models import change_obj_priority
from common.utils.views import add_notification_headers
from common.views import CRUDView, CustomTableView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from job_manager.models.job import JobStatusChoices
from job_manager.models.task import Task, TaskStatusChoices

from microbatching.forms.microbatch_flow import (
    MicrobatchFlowForm,
)
from microbatching.models.microbatch_flow import (
    MicrobatchFlow,
    MicrobatchTaskFlow,
)
from microbatching.services.microbatch_flow import (
    MicrobatchFlowService,
)
from django_q.tasks import async_task

# ------------------------------------------------------------------------------
# Microbatch Views
# ------------------------------------------------------------------------------

MICROBATCH_FLOW_MODEL_FIELDS = [
    "id",
    "order",
    "name",
    "description",
]

MICROBATCH_FLOW_SEARCH_FIELDS = ["id", "name", "description", "notes"]

MICROBATCH_FLOW_MODEL_RELATION_HEADERS = ["TASK_FLOWS", "HISTORY"]

MICROBATCH_FLOW_MODEL_RELATION_FIELDS = {
    "task_flows": {
        "model": MicrobatchTaskFlow,
        "model_name": "microbatch_task_flow_set",
        "related_name": "microbatch_flow",
        "headers": ["ID", "Flow Tasks"],
        "fields": ["id", "name"],
        "show_edit_actions": False,
    },
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "History Date", "History Type", "History User"],
        "fields": ["history_id", "history_date", "history_type", "history_user"],
        "show_edit_actions": False,
    },
}

MICROBATCH_FLOW_TABLE_VIEW = CustomTableView(
    model=MicrobatchFlow,
    model_name="microbatch_flow",
    fields=MICROBATCH_FLOW_MODEL_FIELDS,
    model_relation_headers=MICROBATCH_FLOW_MODEL_RELATION_HEADERS,
    model_relation_fields=MICROBATCH_FLOW_MODEL_RELATION_FIELDS,
    search_fields_list=MICROBATCH_FLOW_SEARCH_FIELDS,
    order_by_field="order",
)

MICROBATCH_FLOW_VIEWS = CRUDView(
    model=MicrobatchFlow,
    model_name="microbatch_flows",
    model_service=MicrobatchFlowService,
    model_form=MicrobatchFlowForm,
    model_table_view=MICROBATCH_FLOW_TABLE_VIEW,
    ordered_model=True,
    list_template_name="microbatching/microbatch_flow/list.html",
)


def match_flows_with_tasks(request):
    """
    Match flows with tasks.
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
        async_task("microbatching.utils.microbatch_flow.create_task_flows")

        response = HttpResponse(status=204)
        response = add_notification_headers(
            response,
            "The task has been started. You will be notified when it's done.",
            "success",
        )
        response["HX-Redirect"] = reverse("microbatch_flows")

        return response
    except Exception as e:
        response = HttpResponse(status=500)
        add_notification_headers(
            response,
            str(e),
            "error",
        )
        return response


def change_microbatch_flow_priority(request, id: int, direction: str):
    """
    Move the rule up or down in the order.

    Parameters:
    -----------
        id: int - The id of the rule.
        direction: str - The direction to move the rule. It can be either "up" or "down".

    Returns:
    --------
        dict: A dictionary containing the message of the operation.
    """

    response = HttpResponse(status=302)
    response["Location"] = reverse("microbatch_flows")

    if direction not in ["up", "down"]:
        response = HttpResponse(status=400)
        message = "Invalid direction. Use 'up' or 'down'."
        add_notification_headers(response, message, "error")
        return response

    try:
        change_obj_priority(model_class=MicrobatchFlow, id=id, direction=direction)

        if request.htmx:
            response = render(
                request,
                "objects/list.html#all-microbatch_flows-table",
                {"rows": MicrobatchFlow.objects.all().order_by("order")},
            )
            return response

        return response

    except MicrobatchFlow.DoesNotExist:
        response = HttpResponse(status=404)
        message = "Microbatch flow not found."
        add_notification_headers(response, message, "error")
        return response

    except Exception as e:
        message = f"An error occurred: {str(e)}"
        add_notification_headers(response, message, "error")
        return response
