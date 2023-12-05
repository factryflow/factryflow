# views.py
from common.utils.views import add_notification_headers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import JobForm
from .models import Job, JobType
from .services import get_all_jobs, job_create_or_update


def show_job_form(request):
    form = JobForm()
    return render(
        request,
        "objects/details.html",
        {"form": form, "button_text": "Add Job", "form_label": "Job Details"},
    )


def show_all_jobs(request):
    jobs = get_all_jobs()
    headers = [
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

    # Create rows as a list of lists
    rows = [
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
        for job in jobs
    ]

    return render(request, "objects/list.html", {"headers": headers, "rows": rows})


@require_http_methods(["POST"])
def save_job_form(request, id: int = None):
    """
    Handle POST request to create or update a job using Django form and service.
    """
    # Get the job instance if updating, else None
    job_instance = get_object_or_404(Job, id=id) if id else None

    # Instantiate the form with POST data and optionally the job instance
    form = JobForm(request.POST, instance=job_instance)

    if form.is_valid():
        # Extract data from the form
        job_data = form.cleaned_data

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
