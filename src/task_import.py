import csv
from datetime import datetime

from django.core.exceptions import ValidationError
from job_manager.models import Job, Task


def import_tasks_from_csv(file_path):
    with open(file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                if (
                    Job.objects.filter(id=row["sales_order_line_key"]).exists()
                    and row["task_uid"]
                ):
                    print(row)
                    start = row["planned_task_start"].split(".")[0]
                    start_datetime = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")

                    end = row["planned_task_end"].split(".")[0]
                    end_datetime = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

                    task = Task(
                        name=row["task_uid"],
                        planned_start_datetime=start_datetime,
                        planned_end_datetime=end_datetime,
                        job_id=row["sales_order_line_key"],
                        # test data below
                        duration=500,
                        setup_time=480,
                        teardown_time=480,
                        quantity=1,
                        item_id=3,
                        # Add more fields as needed
                    )
                    task.full_clean()  # Validate the task data
                    task.save()  # Save the task to the database
                    print("TASK CREATED")
            except (KeyError, ValidationError) as e:
                print(f"Error importing task: {e}")


# Usage example
csv_file_path = "/workspaces/factryflow/src/tasks_v2.csv"
import_tasks_from_csv(csv_file_path)
