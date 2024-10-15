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
    MicrobatchTask,
    MicrobatchTaskFlow,
)
from microbatching.services.microbatch_flow import (
    MicrobatchFlowService,
)

# ------------------------------------------------------------------------------
# Microbatch Views
# ------------------------------------------------------------------------------

MICROBATCH_FLOW_MODEL_FIELDS = [
    "id",
    "name",
    "description",
]
MICROBATCH_FLOW_TABLE_HEADERS = [
    "ID",
    "Name",
    "Description",
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
    headers=MICROBATCH_FLOW_TABLE_HEADERS,
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


def generate_task_predecessors_flow(
    start_rule, end_task, min_flow_length, max_flow_length, task_flow_list=[]
):
    """Generates a list of tasks based on predecessors and flow settings."""

    if end_task.predecessors.count() == 0:
        task_flow_list.append(end_task)
        if len(task_flow_list) > 0:
            if (
                len(task_flow_list) >= min_flow_length
                and len(task_flow_list) <= max_flow_length
            ):  # Check if the flow length is within the limits
                if (
                    task_flow_list[-1]
                    .microbatchruletaskmatch_set.filter(microbatch_rule=start_rule)
                    .exists()
                ):  # Check if the last Task in the flow matches the start rule
                    # breakpoint()
                    return task_flow_list
        return []
    else:
        task_flow_list.append(end_task)
        return generate_task_predecessors_flow(
            start_rule=start_rule,
            end_task=end_task.predecessors.first(),
            min_flow_length=min_flow_length,
            max_flow_length=max_flow_length,
            task_flow_list=task_flow_list,
        )


def create_task_flows(microbatch_flow, tasks):
    """Create MicrobatchTaskFlows based on selected MicrobatchFlow and Tasks."""
    try:
        matching_task_count = 0

        for task in tasks:
            # Check Task predecessors
            end_task = None

            if task.microbatchruletaskmatch_set.filter(
                microbatch_rule=microbatch_flow.end_rule
            ).exists():
                end_task = task

                if end_task.predecessors.count():
                    task_flow_list = generate_task_predecessors_flow(
                        start_rule=microbatch_flow.start_rule,
                        end_task=end_task,
                        min_flow_length=microbatch_flow.min_flow_length,
                        max_flow_length=microbatch_flow.max_flow_length,
                        task_flow_list=[],  # Reset the task_flow_list for every end_task
                    )

                    if task_flow_list:
                        task_flow = MicrobatchTaskFlow.objects.create(
                            microbatch_flow=microbatch_flow
                        )
                        matching_task_count += 1
                        order_index = len(task_flow_list)
                        for task in task_flow_list:
                            MicrobatchTask.objects.create(
                                task=task,
                                microbatch_task_flow=task_flow,
                                order=order_index,
                            )
                            order_index -= 1
                        print(task_flow_list)

        return f"Generated {matching_task_count} TaskFlows with MicrobatchFlow ID: {microbatch_flow.id}"
    except Exception as e:
        raise e


def create_all_task_flows(tasks):
    """Create MicrobatchTaskFlows based on all MicrobatchFlows and a list of Tasks."""
    try:
        MicrobatchTaskFlow.objects.all().delete()
        MicrobatchTask.objects.all().delete()
        result = {}
        message_list = []

        for flow in MicrobatchFlow.objects.all():
            message_list.append(create_task_flows(flow, tasks))

        if message_list:
            result["message"] = "\n".join(message_list)
        else:
            result["message"] = "No Tasks matched with any MicrobatchFlow"
        result["status"] = "success"

        return result

    except Exception as e:
        result["message"] = str(e)
        result["status"] = "error"
        return result


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

        result = create_all_task_flows(tasks)

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
