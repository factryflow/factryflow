# Fields that are not required in the form
NOT_REQUIRED_FIELDS_IN_FORM = [
    "created_at",
    "updated_at",
    "created_by",
    "updated_by",
    "custom_fields",
]


def get_html_input_type(field_type):
    """
    Convert Django model field types to HTML input types.

    Args:
        field_type (str): The internal type of the Django model field.

    Returns:
        str: The corresponding HTML input type.
    """
    if field_type == "CharField":
        return "text"
    elif field_type == "TextField":
        return "textarea"
    elif field_type == "EmailField":
        return "email"
    elif field_type == "URLField":
        return "url"
    elif field_type == "IntegerField":
        return "number"
    elif field_type == "FloatField":
        return "number"
    elif field_type == "DecimalField":
        return "number"
    elif field_type == "BooleanField":
        return "checkbox"
    elif field_type == "DateField":
        return "date"
    elif field_type == "DateTimeField":
        return "datetime-local"
    elif field_type == "TimeField":
        return "time"
    elif field_type == "FileField":
        return "file"
    elif field_type == "ImageField":
        return "file"
    elif field_type == "ForeignKey":
        return "number"
    else:
        return "text"
