# views.py
from common.utils.views import add_notification_headers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import JobForm
from .models import Job, JobType
from .services import delete_job, get_all_jobs, job_create_or_update


class JobTableView:
    def __init__(self):
        self.jobs = get_all_jobs()

    @property
    def table_headers(self):
        return [
            "Job ID",
            "Job Name",
            "Description",
            "Customer",
            "Due Date",
            "Planned Start",
            "Planned End",
            "Priority",
            "Status",
        ]

    @property
    def table_rows(self):
        return [
            [
                job.id,
                job.name,
                job.description,
                job.customer,
                job.due_date.strftime("%Y-%m-%d") if job.due_date else "",
                job.planned_start_datetime.strftime("%Y-%m-%d")
                if job.planned_start_datetime
                else "",
                job.planned_end_datetime.strftime("%Y-%m-%d")
                if job.planned_end_datetime
                else "",
                job.priority,
                job.get_job_status_display(),
            ]
            for job in self.jobs
        ]


def show_job_form(request, id: int = None, edit: str = ""):
    form_action_url = "/job-create/"

    if id:
        job = get_object_or_404(Job, id=id)
        form = JobForm(instance=job)

        if edit != "T":
            view_mode = True
            form_label = "View Job"
            button_text = "Edit"
            edit_url = reverse("edit_job", args=[id, "T"])

            # Make all form fields read-only
            for field in form.fields.values():
                field.widget.attrs["readonly"] = True

        else:
            button_text = "Save"
            form_label = "Edit Job"
            view_mode = False

    else:
        form = JobForm()
        button_text = "Create Job"
        view_mode = False
        form_label = "New Job Details"

    context = {
        "form": form,
        "view_mode": view_mode,
        "form_label": form_label,
        "button_text": button_text,
        "form_action_url": form_action_url,
        "id": id if id else None,
        "edit_url": edit_url if "edit_url" in locals() else "#",
    }

    return render(
        request,
        "objects/details.html",
        context,
    )


def show_all_jobs(request):
    table = JobTableView()
    return render(
        request,
        "objects/list.html",
        {"headers": table.table_headers, "rows": table.table_rows},
    )


@require_http_methods(["POST"])
def save_job_form(request, id: int = None):
    """
    Handle POST request to create or update a job using Django form and service.
    """
    # Get the job instance if updating, else None
    job_instance = get_object_or_404(Job, id=id) if id else None

    # Instantiate the form with POST data and optionally the job instance
    form = JobForm(request.POST, instance=job_instance)
    id = request.POST.get("id")

    if form.is_valid():
        # Extract data from the form
        job_data = form.cleaned_data
        job_data["id"] = id

        # Prepare additional data for the service function, if needed
        job_type = JobType.objects.get(id=1)

        # Call the service function
        job = job_create_or_update(job_data=job_data, job_type=job_type)

        form = JobForm()
        response = render(
            request,
            "objects/details.html#partial-form",
            {"form": form, "button_text": "Add Job", "form_label": "Job Details"},
        )
        # add_notification_headers(response, "Job created successfully!", "success")

        # return response
        # If the request is from htmx
        if request.htmx:
            headers = {
                "HX-Redirect": reverse(
                    "job"
                )  # This is where you want to redirect after success
            }
            response = HttpResponse(status=204, headers=headers)
            add_notification_headers(response, "Job created successfully!", "success")
            return response


def request_job_delete(request, id: int):
    """
    Handle job deletion request. Deletes a job based on the given ID,
    retrieves the updated job list, and returns a response with a notification.
    """
    delete_job(id=id)
    table = JobTableView()
    response = render(
        request,
        "objects/list.html#partial-table-template",
        {"headers": table.table_headers, "rows": table.table_rows},
    )
    add_notification_headers(response, "Job has been deleted.", "info")
    return response
