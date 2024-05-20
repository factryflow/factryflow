from django.core.management.base import BaseCommand
from data_seeding_scripts.utils.get_data_from_csv import add_data_from_csv

from job_manager.models import JobType, TaskType, WorkCenter, Item
from resource_calendar.models import (
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
    OperationalExceptionType,
)



# models_details - list of dictionaries containing model_name, model, and file_name
models_details = [
    {"model_name": "JobType", "model": JobType, "file_name": "job_type.csv"},
    {"model_name": "TaskType", "model": TaskType, "file_name": "task_type.csv"},
    {"model_name": "WorkCenter", "model": WorkCenter, "file_name": "work_center.csv"},
    {"model_name": "Item", "model": Item, "file_name": "item.csv"},
    {
        "model_name": "WeeklyShiftTemplate",
        "model": WeeklyShiftTemplate,
        "file_name": "shift_template.csv",
    },
    {
        "model_name": "WeeklyShiftTemplateDetail",
        "model": WeeklyShiftTemplateDetail,
        "file_name": "shift_details.csv",
    },
    {
        "model_name": "OperationalExceptionType",
        "model": OperationalExceptionType,
        "file_name": "exception_type.csv",
    },
]


class Command(BaseCommand):
    """
    CUSTOM COMMAND TO ADD DATA
    --------------------------
        This command adds data from CSV files to the database.
    """

    help = "Adds data from CSV files to the database"

    def handle(self, *args, **options):
        for model_detail in models_details:
            model_name = model_detail["model_name"]
            model = model_detail["model"]
            file_name = model_detail["file_name"]
            result = add_data_from_csv(model, file_name)
            self.stdout.write(
                f"Added data for {model_name}: {result['status']} - {result['message']}"
            )
