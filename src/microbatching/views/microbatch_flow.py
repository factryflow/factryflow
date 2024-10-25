from common.utils.views import add_notification_headers
from common.views import CRUDView, CustomTableView
from django.http import HttpResponse

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
from microbatching.utils.microbatch_flow import create_task_flows

# ------------------------------------------------------------------------------
# Microbatch Views
# ------------------------------------------------------------------------------

MICROBATCH_FLOW_MODEL_FIELDS = [
    "id",
    "name",
    "description",
]

MICROBATCH_FLOW_SEARCH_FIELDS = ["name"]

MICROBATCH_FLOW_MODEL_RELATION_HEADERS = ["TASK_FLOWS", "HISTORY"]

MICROBATCH_FLOW_MODEL_RELATION_FIELDS = {
    "task_flows": {
        "model": MicrobatchTaskFlow,
        "model_name": "microbatch_task_flow_set",
        "related_name": "microbatch_flow",
        "headers": ["ID", "TASK_FLOWS"],
        "fields": ["id", "task_flows"],
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
)

MICROBATCH_FLOW_VIEWS = CRUDView(
    model=MicrobatchFlow,
    model_name="microbatch_flows",
    model_service=MicrobatchFlowService,
    model_form=MicrobatchFlowForm,
    model_table_view=MICROBATCH_FLOW_TABLE_VIEW,
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

        result = create_task_flows()

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
