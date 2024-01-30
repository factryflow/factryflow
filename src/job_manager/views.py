# views.py
from common.utils.views import add_notification_headers
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import JobForm
from .models import Job, JobType
from .services import JobService
from common.views import CRUDView

# ------------------------------------------------------------------------------
# Job Views
# ------------------------------------------------------------------------------


class JobTableView:
    """
    Class representing a view for displaying jobs in a table format
    """

    def __init__(self, status_filter=None, search_query=None):
        """
        Initialization of the class with optional filtering parameters.
        """
        self.jobs = Job.objects.all()
        self.status_filter = status_filter if status_filter else "all"
        self.search_query = search_query

    @property
    def filtered_jobs(self):
        """
        Property to get filtered job list based on status and search query.
        """
        jobs = self.jobs
        if self.status_filter != "all":
            jobs = [job for job in jobs if job.job_status == self.status_filter]
        if self.search_query:
            jobs = [
                job
                for job in jobs
                if self.search_query.lower() in job.name.lower()
                or self.search_query.lower() in job.description.lower()
                or self.search_query.lower() in job.customer.lower()
                or str(self.search_query) in str(job.id)
            ]
        return jobs

    @property
    def table_headers(self):
        """
        Property to define table headers for the job list.
        """
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
        """
        Property to get the rows of data for the job table based on filtered jobs.
        """
        return [
            [
                job.id,  # As much as possible, we put the table id first
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
                f'<span class="{self.get_status_colored_text(job.job_status)} text-xs font-medium px-2 py-0.5 rounded whitespace-nowrap">{job.get_job_status_display()}</span>',
            ]
            for job in self.filtered_jobs
        ]

    def get_status_colored_text(self, job_status):
        """
        Method to get the colored text based on job status.
        """
        # You can customize this part based on your specific job status and colors
        tailwind_classes = {
            "CM": "bg-haxgreen text-[#3DAD99]",
            "NP": "bg-haxred text-[#FF4D4F]",
            "IP": "bg-haxyellow text-[#F6C000]",
            "CN": "bg-haxpurple text-[#7239EA]",
        }
        return tailwind_classes.get(job_status)


JOB_VIEWS = CRUDView(
    model=Job,
    model_type=JobType,
    model_name="job",
    model_service=JobService,
    model_form=JobForm,
    model_table_view=JobTableView,
)