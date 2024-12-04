# Fields that are not required in the form
NOT_REQUIRED_FIELDS_IN_FORM = [
    "created_at",
    "updated_at",
    "created_by",
    "updated_by",
    "custom_fields",
]


HTML_INPUT_TYPES = {
    "CharField": "text",
    "TextField": "textarea",
    "EmailField": "email",
    "URLField": "url",
    "IntegerField": "number",
    "FloatField": "number",
    "DecimalField": "number",
    "BooleanField": "checkbox",
    "DateField": "date",
    "DateTimeField": "datetime-local",
    "TimeField": "time",
    "FileField": "file",
    "ImageField": "file",
    "ForeignKey": "number",
}


# nested criteria management models list
NESTED_CRITERIA_RELATED_MODELS = ["microbatch_rules", "assigment_rules"]
