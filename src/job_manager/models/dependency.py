from common.models import BaseModel
from django.db import models


class DependencyStatus(BaseModel):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = "dependency_status"


class DependencyType(BaseModel):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = "dependency_type"


class Dependency(BaseModel):
    name = models.CharField(max_length=150)
    external_id = models.CharField(max_length=180, blank=True, null=True)
    expected_close_datetime = models.DateTimeField(blank=True, null=True)
    actual_close_datetime = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    dependency_type = models.ForeignKey(DependencyType, on_delete=models.DO_NOTHING)
    dependency_status = models.ForeignKey(DependencyStatus, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "dependency"
