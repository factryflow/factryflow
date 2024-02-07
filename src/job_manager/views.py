# views.py

from common.views import CRUDView, CustomTableView

from .forms import JobForm, TaskForm, DependencyForm
from .models import Job, JobType, Task, TaskType, Dependency, DependencyType
from .services import JobService, TaskService, DependencyService

# ------------------------------------------------------------------------------
# Job Views
# ------------------------------------------------------------------------------


# class JobTableView:
#     """
#     Class representing a view for displaying jobs in a table format
#     """

#     def __init__(self, status_filter=None, search_query=None):
#         """
#         Initialization of the class with optional filtering parameters.
#         """
#         self.jobs = Job.objects.all()
#         self.status_filter = status_filter if status_filter else "all"
#         self.search_query = search_query

#     @property
#     def filtered_jobs(self):
#         """
#         Property to get filtered job list based on status and search query.
#         """
#         jobs = self.jobs
#         if self.status_filter != "all":
#             jobs = [job for job in jobs if job.job_status == self.status_filter]
#         if self.search_query:
#             jobs = [
#                 job
#                 for job in jobs
#                 if self.search_query.lower() in job.name.lower()
#                 or self.search_query.lower() in job.description.lower()
#                 or self.search_query.lower() in job.customer.lower()
#                 or str(self.search_query) in str(job.id)
#             ]
#         return jobs

#     @property
#     def table_headers(self):
#         """
#         Property to define table headers for the job list.
#         """
#         return [
#             "Job ID",
#             "Job Name",
#             "Description",
#             "Customer",
#             "Due Date",
#             "Planned Start",
#             "Planned End",
#             "Priority",
#             "Status",
#         ]

#     @property
#     def table_rows(self):
#         """
#         Property to get the rows of data for the job table based on filtered jobs.
#         """
#         return [
#             [
#                 job.id,  # As much as possible, we put the table id first
#                 job.name,
#                 job.description,
#                 job.customer,
#                 job.due_date.strftime("%Y-%m-%d") if job.due_date else "",
#                 job.planned_start_datetime.strftime("%Y-%m-%d")
#                 if job.planned_start_datetime
#                 else "",
#                 job.planned_end_datetime.strftime("%Y-%m-%d")
#                 if job.planned_end_datetime
#                 else "",
#                 job.priority,
#                 f'<span class="{self.get_status_colored_text(job.job_status)} text-xs font-medium px-2 py-0.5 rounded whitespace-nowrap">{job.get_job_status_display()}</span>',
#             ]
#             for job in self.filtered_jobs
#         ]

#     def get_status_colored_text(self, job_status):
#         """
#         Method to get the colored text based on job status.
#         """
#         # You can customize this part based on your specific job status and colors
#         tailwind_classes = {
#             "CM": "bg-haxgreen text-[#3DAD99]",
#             "NP": "bg-haxred text-[#FF4D4F]",
#             "IP": "bg-haxyellow text-[#F6C000]",
#             "CN": "bg-haxpurple text-[#7239EA]",
#         }
#         return tailwind_classes.get(job_status)


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
JOB_TABLE_HEADERS = [
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

JobTableView = CustomTableView(
    model=Job,
    model_name="job",
    fields=JOB_MODEL_FIELDS,
    headers=JOB_TABLE_HEADERS,
    status_filter_field=JOB_STATUS_FILTER_FIELD,
    search_fields_list=JOB_SEARCH_FIELDS,
    tailwind_classes=JOB_TAILWIND_CLASSES,
)


JOB_VIEWS = CRUDView(
    model=Job,
    model_type=JobType,
    model_name="job",
    model_service=JobService,
    model_form=JobForm,
    model_table_view=JobTableView,
)


# ------------------------------------------------------------------------------
# Task Views
# ------------------------------------------------------------------------------

TASK_MODEL_FIELDS = [
    "id",
    "name",
    "setup_time",
    "run_time_per_unit",
    "teardown_time",
    "quantity",
    "planned_start_datetime",
    "planned_end_datetime",
    "item",
    "task_status",
]

TASK_TAILWIND_CLASSES = {
    "NS": "bg-haxred text-[#FF4D4F]",
    "IP": "bg-haxyellow text-[#F6C000]",
    "CM": "bg-haxgreen text-[#3DAD99]",
}

TASK_STATUS_FILTER_FIELD = "task_status"
TASK_SEARCH_FIELDS = ["name", "item", "id"]
TASK_TABLE_HEADERS = [
    "Task ID",
    "Task Name",
    "Setup Time",
    "Run Time Per Unit",
    "Teardown Time",
    "Quantity",
    "Planned Start",
    "Planned End",
    "Item",
    "Status",
]

TaskTableView = CustomTableView(
    model=Task,
    model_name="task",
    fields=TASK_MODEL_FIELDS,
    headers=TASK_TABLE_HEADERS,
    status_filter_field=TASK_STATUS_FILTER_FIELD,
    search_fields_list=TASK_SEARCH_FIELDS,
    tailwind_classes=TASK_TAILWIND_CLASSES,
)

TASK_VIEWS = CRUDView(
    model=Task,
    model_type=TaskType,
    model_name="task",
    model_service=TaskService,
    model_form=TaskForm,
    model_table_view=TaskTableView,
)



# ------------------------------------------------------------------------------
# Dependecy Views
# ------------------------------------------------------------------------------

DEPENDENCY_MODEL_FIELDS = [
    "id",
    "name",
    "expected_close_datetime",
    "actual_close_datetime",
    "dependency_type",
    "dependency_status",
]

DEPENDENCY_TAILWIND_CLASSES = {
    "PD": "bg-haxred text-[#FF4D4F]",
    "IP": "bg-haxyellow text-[#F6C000]",
    "RS": "bg-haxgreen text-[#3DAD99]",
    "CN": "bg-haxpurple text-[#7239EA]",
}

DEPENDENCY_STATUS_FILTER_FIELD = "dependency_status"
DEPENDENCY_SEARCH_FIELDS = ["name", "id"]
DEPENDENCY_TABLE_HEADERS = [
    "Dependency ID",
    "Dependency Name",
    "Expected Close",
    "Actual Close",
    "Type",
    "Status",
]

DependencyTableView = CustomTableView(
    model=Dependency,
    model_name="dependency",
    fields=DEPENDENCY_MODEL_FIELDS,
    headers=DEPENDENCY_TABLE_HEADERS,
    status_filter_field=DEPENDENCY_STATUS_FILTER_FIELD,
    search_fields_list=DEPENDENCY_SEARCH_FIELDS,
    tailwind_classes=DEPENDENCY_TAILWIND_CLASSES,
)

DEPENDENCY_VIEWS = CRUDView(
    model=Dependency,
    model_type=DependencyType,
    model_name="dependency",
    model_service=DependencyService,
    model_form=DependencyForm,
    model_table_view=DependencyTableView,
)

