import csv
import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
from job_manager.models import Job, JobType


def import_jobs_from_csv(file_path):
    # create a datetime which is timezone aware and 10 days from now
    add_days = datetime.timedelta(days=20)
    due_date = timezone.now() + add_days

    job_type = JobType.objects.first()
    priority = 1

    with open(file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                job = Job(
                    id=row["job_id"],
                    name=row["job_name"],
                    due_date=due_date,
                    job_type=job_type,
                    priority=priority,
                )
                job.full_clean()  # Validate the task data
                job.save()  # Save the task to the database
                priority += 1
            except (KeyError, ValidationError) as e:
                print(f"Error importing task: {e}")


# Usage example
csv_file_path = "/workspaces/factryflow/src/jobs_v2.csv"
import_jobs_from_csv(csv_file_path)
