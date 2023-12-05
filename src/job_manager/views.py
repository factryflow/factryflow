# views.py
from common.utils.views import add_notification_headers
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import JobForm
from .models import Job, JobType
from .services import job_create_or_update


def show_job_form(request):
    form = JobForm()
    return render(
        request,
        "objects/details.html",
        {"form": form, "button_text": "Add Job", "form_label": "Job Details"},
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
        add_notification_headers(response, "Job created successfully!", "success")

        return response

    # Re-render the form with errors if it's not valid
    # template_name = (
    #     "job_manager/forms/form_add_job.html"
    #     if not id
    #     else "job_manager/forms/form_edit_job.html"
    # )
    # return render(request, template_name, {"form": form})
