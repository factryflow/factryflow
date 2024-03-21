# Generated by Django 4.2.7 on 2024-03-11 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("job_manager", "0006_historicaltask_duration_task_duration"),
        ("resource_manager", "0008_alter_historicalresource_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SchedulerRuns",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField(blank=True, null=True)),
                ("run_duration", models.DurationField(blank=True, null=True)),
                ("details", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ST", "Started"),
                            ("CP", "Completed"),
                            ("FL", "Failed"),
                            ("CN", "Cancelled"),
                        ],
                        default="ST",
                        max_length=2,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(class)s_objects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_%(class)s_objects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "scheduler_runs",
            },
        ),
        migrations.CreateModel(
            name="ResourceIntervals",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("interval_start", models.DateTimeField()),
                ("interval_end", models.DateTimeField()),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(class)s_objects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "resource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="resource_manager.resource",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="job_manager.task",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_%(class)s_objects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "resource_intervals",
            },
        ),
        migrations.CreateModel(
            name="ResourceAllocations",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(class)s_objects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "resource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="resource_manager.resource",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="job_manager.task",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_%(class)s_objects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "resource_allocations",
            },
        ),
    ]
