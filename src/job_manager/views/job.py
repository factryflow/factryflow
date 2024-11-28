# views.py
import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Case, When, Value, IntegerField
from django.db import transaction
from django.http import HttpResponse

from common.views import CRUDView, CustomTableView
from common.utils.views import add_notification_headers

from job_manager.forms import (
    JobForm,
    JobTypeForm,
)
from job_manager.models import (
    Job,
    JobStatusChoices,
    JobType,
    Task,
)
from job_manager.services import (
    JobService,
    JobTypeService,
)


# ------------------------------------------------------------------------------
# Job Type Views
# ------------------------------------------------------------------------------

JOB_TYPE_MODEL_FIELDS = ["id", "name", "notes"]

JOB_TYPE_SEARCH_FIELDS = ["name", "notes", "id"]

JOB_TYPE_MODEL_RELATION_HEADERS = ["HISTORY"]
JOB_TYPE_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "Name", "User", "Notes", "History Date"],
        "fields": ["history_id", "name", "history_user", "notes", "history_date"],
        "show_edit_actions": False,
    },
}

JOB_TYPE_TABLE_VIEW = CustomTableView(
    model=JobType,
    model_name="job_type",
    fields=JOB_TYPE_MODEL_FIELDS,
    model_relation_headers=JOB_TYPE_MODEL_RELATION_HEADERS,
    model_relation_fields=JOB_TYPE_MODEL_RELATION_FIELDS,
    search_fields_list=JOB_TYPE_SEARCH_FIELDS,
)

JOB_TYPE_VIEWS = CRUDView(
    model=JobType,
    model_name="job_types",
    model_service=JobTypeService,
    model_form=JobTypeForm,
    model_table_view=JOB_TYPE_TABLE_VIEW,
)


# ------------------------------------------------------------------------------
# Job Views
# ------------------------------------------------------------------------------

JOB_TAILWIND_CLASSES = {
    "CM": "bg-haxgreen text-[#3DAD99]",
    "NP": "bg-haxred text-[#FF4D4F]",
    "IP": "bg-haxyellow text-[#F6C000]",
    "CN": "bg-haxpurple text-[#7239EA]",
}

JOB_MODEL_FIELDS = [
    "id",
    "name",
    "description",
    "customer",
    "due_date",
    "planned_start_datetime",
    "planned_end_datetime",
    "priority",
    "job_status",
]

JOB_STATUS_FILTER_FIELD = "job_status"
JOB_SEARCH_FIELDS = ["name", "description", "customer", "id"]

JOB_MODEL_RELATION_HEADERS = ["TASKS", "DEPENDENCIES", "HISTORY"]

JOB_MODEL_RELATION_FIELDS = {
    # model_name: [model, related_name, [headers], [fields]]
    "tasks": {
        "model": Task,
        "model_name": "task",
        "related_name": "job",
        "headers": [
            "ID",
            "Task Name",
            "Item",
            "Quantity",
            "Run Time",
            "Planned Start",
            "Planned End",
            "Task Type",
            "Status",
        ],
        "fields": [
            "id",
            "name",
            "item",
            "quantity",
            "run_time_per_unit",
            "planned_start_datetime",
            "planned_end_datetime",
            "task_type",
            "task_status",
        ],
        "show_edit_actions": False,
    },
    "dependencies": {
        "model_name": "dependency",
        "related_name": "dependencies",
        "headers": [
            "ID",
            "Dependency Name",
            "Expected Close",
            "Actual Close",
            "Type",
            "Status",
        ],
        "fields": [
            "id",
            "name",
            "expected_close_datetime",
            "actual_close_datetime",
            "dependency_type",
            "dependency_status",
        ],
        "show_edit_actions": False,
    },
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": [
            "ID",
            "Name",
            "User",
            "Customer",
            "Due Date",
            "Description",
            "Notes",
            "History Date",
        ],
        "fields": [
            "history_id",
            "name",
            "history_user",
            "customer",
            "due_date",
            "description",
            "notes",
            "history_date",
        ],
        "show_edit_actions": False,
    },
}


JOB_TABLE_VIEW = CustomTableView(
    model=Job,
    model_name="job",
    fields=JOB_MODEL_FIELDS,
    status_choices_class=JobStatusChoices,
    model_relation_headers=JOB_MODEL_RELATION_HEADERS,
    model_relation_fields=JOB_MODEL_RELATION_FIELDS,
    status_filter_field=JOB_STATUS_FILTER_FIELD,
    search_fields_list=JOB_SEARCH_FIELDS,
    tailwind_classes=JOB_TAILWIND_CLASSES,
)


JOB_VIEWS = CRUDView(
    model=Job,
    model_type=JobType,
    model_name="jobs",
    model_service=JobService,
    model_form=JobForm,
    model_table_view=JOB_TABLE_VIEW,
)


# ------------------------------------------------------------------------------
# Job Priority manager
# ------------------------------------------------------------------------------


def job_prioritization_view(request):
    """
    Job Prioritization View
    """
    if request.user.require_password_change:
        return redirect(reverse("users:change_password"))

    if request.htmx:
        try:
            job_data = json.loads(request.POST.get("job_data"))

            with transaction.atomic():
                for job in job_data:
                    job_obj = Job.objects.get(id=job["id"])
                    if "due_date" in job:
                        job_obj.due_date = job["due_date"]
                    if "manual_priority" in job:
                        job_obj.manual_priority = job["manual_priority"]
                    job_obj.save()
        except Exception as e:
            response = HttpResponse(status=400)
            add_notification_headers(
                response,
                str(e),
                "success",
            )

    jobs = (
        Job.objects.exclude(job_status__in=["CM", "CN"])
        .annotate(
            sort_priority=Case(
                When(priority__isnull=True, then=Value(999999)),
                default="priority",
                output_field=IntegerField(),
            )
        )
        .order_by("sort_priority")
    )

    context = {
        "jobs": jobs,
        "view_mode": "false",
        "status_filter_dict": {
            "NP": "Not Planned",
            "IP": "In Progress",
        },
    }

    if request.htmx:
        return render(
            request, "job/prioritization.html#partial-table-template", context
        )

    return render(
        request,
        "job/prioritization.html",
        context,
    )
