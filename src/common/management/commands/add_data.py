from job_manager.models import JobType, TaskType, WorkCenter, Item
from resource_manager.models import Resource, ResourceGroup
from resource_calendar.models import (
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
    OperationalException,
)
from django.core.management.base import BaseCommand
from data_seeding_scripts.utils.get_data_from_csv import add_data_from_csv


# models_details - list of dictionaries containing model_name, model, and file_name
models_details = [
    {"model_name": "JobType", "model": JobType, "file_name": "job_type.csv"},
    {"model_name": "TaskType", "model": TaskType, "file_name": "task_type.csv"},
    {"model_name": "WorkCenter", "model": WorkCenter, "file_name": "work_center.csv"},
    {"model_name": "Item", "model": Item, "file_name": "item.csv"},
    {"model_name": "Resource", "model": Resource, "file_name": "resource.csv"},
    {
        "model_name": "ResourceGroup",
        "model": ResourceGroup,
        "file_name": "resource_group.csv",
    },
    {
        "model_name": "WeeklyShiftTemplate",
        "model": WeeklyShiftTemplate,
        "file_name": "weekly_shift_template.csv",
    },
    {
        "model_name": "WeeklyShiftTemplateDetail",
        "model": WeeklyShiftTemplateDetail,
        "file_name": "weekly_shift_template_detail.csv",
    },
    {
        "model_name": "OperationalException",
        "model": OperationalException,
        "file_name": "operational_exception.csv",
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
