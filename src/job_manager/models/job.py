# Create your models here.
from common.models import BaseModel
from django.db import models
from ordered_model.models import OrderedModelBase


class JobStatus(BaseModel):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = "job_status"


class JobType(BaseModel):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = "job_type"


class Job(BaseModel, OrderedModelBase):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    customer = models.CharField(max_length=250, blank=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.PositiveIntegerField(editable=False, db_index=True)
    order_field_name = "priority"
    planned_start_datetime = models.DateTimeField(null=True, blank=True)
    planned_end_datetime = models.DateTimeField(null=True, blank=True)
    external_id = models.CharField(max_length=150, blank=True)
    note = models.CharField(max_length=150, blank=True)
    job_status = models.ForeignKey(JobStatus, on_delete=models.DO_NOTHING)
    job_type = models.ForeignKey(JobType, on_delete=models.DO_NOTHING)
    dependencies = models.ManyToManyField("Dependency", related_name="jobs")

    class Meta:
        db_table = "job"
        ordering = ("priority",)
