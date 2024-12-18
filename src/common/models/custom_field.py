import re

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords

from .base import BaseModel


class FieldType(models.TextChoices):
    TEXT = "text", "Text"
    NUMBER = "number", "number"
    DATE = "date", "Date"
    TIME = "time", "Time"
    DATETIME = "datetime-local", "Datetime-local"
    # Add more field types here if required

    @classmethod
    def to_dict(cls):
        """
        Convert the RESOURCE_TYPES class into a dictionary.

        Returns:
        - Dictionary where choice values are keys and choice descriptions are values.
        """
        return {choice[0]: choice[1] for choice in cls.choices}


class CustomField(BaseModel):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="custom_fields"
    )
    name = models.CharField(max_length=150)
    label = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    field_type = models.CharField(max_length=20, choices=FieldType.choices)
    is_required = models.BooleanField(default=False)

    history = HistoricalRecords(table_name="custom_field_history")

    class Meta:
        db_table = "custom_field"
        unique_together = [["content_type", "name"]]

    def clean(self):
        """Validate field data."""
        self._validate_custom_field_name(self.name)

    def _validate_custom_field_name(self, value):
        if not re.match(r"^[a-z]+(?:_[a-z]+)*$", value):
            raise ValidationError("Field name must be snake_case. Example: my_field")
