import os
import pandas as pd


def add_data_from_csv(model, file_name):
    try:
        # create file path - file is in data_seeding_scripts/csv_data folder
        file_path = os.path.join(
            "/workspaces/factryflow/src/", "static", "csv_data", file_name
        )

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Get the field names from df headers of file
        field_names = df.columns.tolist()

        # Create instances using field_names and add them to the data list
        data = []
        for _, row in df.iterrows():
            row_data = {field_name: row[field_name] for field_name in field_names}
            # Check if data already exists
            if not model.objects.filter(**row_data).exists():
                data.append(model(**row_data))

        # Bulk create the objects
        model.objects.bulk_create(data)

        # # Add many-to-many fields using the Django ORM set method
        # if m2m_fields:
        #     for field_name in m2m_fields:
        #         for obj in model.objects.all():
        #             m2m_field = getattr(obj, field_name)
        #             m2m_field.set([related_obj.id for related_obj in m2m_field.all()])

        # Return success status and message
        return {"status": "success", "message": "Data added successfully."}

    except Exception as e:
        # Return error status and message
        return {"status": "error", "message": str(e)}
