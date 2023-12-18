import re

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        related_name="created_%(class)s_objects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        User,
        related_name="updated_%(class)s_objects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        if not self.pk and user:
            self.created_by = user
        if user:
            self.updated_by = user
        super().save(*args, **kwargs)


class FieldType:
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"

    CHOICES = [
        (TEXT, "Text"),
        (NUMBER, "Number"),
        (DATE, "Date"),
        # Add other types as needed
    ]


class CustomField(BaseModel):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="custom_fields"
    )
    name = models.CharField(max_length=150)
    label = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    field_type = models.CharField(max_length=10, choices=FieldType.CHOICES)
    is_required = models.BooleanField(default=False)

    history = HistoricalRecords(table_name="custom_field_history")

    class Meta:
        db_table = "custom_field"
        unique_together = [["content_type", "name"]]

    def clean(self):
        """Validate field data."""
        self._validate_snake_case(self.name)

    def _validate_snake_case(value):
        if not re.match(r"^[a-z]+(?:_[a-z]+)*$", value):
            raise ValidationError("Field name must be in snake_case. Example: my_field")
