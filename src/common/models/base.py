from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_%(class)s_objects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="updated_%(class)s_objects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    # add jsonb field for storing extra data - create a reatable variable named extras
    custom_fields = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        if not self.pk and user:
            self.created_by = user
        if user:
            self.updated_by = user
        super().save(*args, **kwargs)


class BaseModelWithExtras(BaseModel):
    external_id = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True
