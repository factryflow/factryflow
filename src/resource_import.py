import csv

from django.core.exceptions import ValidationError
from resource_manager.models import Resource


def import_resources_from_csv(file_path):
    with open(file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                resource = Resource(
                    name=row["Title"],
                    # Add more fields as needed
                )
                resource.full_clean()  # Validate the resource data
                resource.save()  # Save the resource to the database
            except (KeyError, ValidationError) as e:
                print(f"Error importing resource: {e}")


# Usage example
csv_file_path = "/workspaces/factryflow/src/resources.csv"
import_resources_from_csv(csv_file_path)
