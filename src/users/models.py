from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "self", on_delete=models.DO_NOTHING, blank=True, null=True
    )
    require_password_change = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        if user:
            self.updated_by = user
        super().save(*args, **kwargs)
