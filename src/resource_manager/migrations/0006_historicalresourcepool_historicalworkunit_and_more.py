# Generated by Django 4.2.7 on 2024-01-17 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):
    dependencies = [
        ("resource_assigner", "0006_remove_assigmentrule_resource_group_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("resource_manager", "0005_historicalresource_notes_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalResourcePool",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("updated_at", models.DateTimeField(blank=True, editable=False)),
                ("external_id", models.CharField(blank=True, max_length=50)),
                ("notes", models.TextField(blank=True)),
                ("name", models.CharField(max_length=100)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical resource pool",
                "verbose_name_plural": "historical resource pools",
                "db_table": "resource_pool_history",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalWorkUnit",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("updated_at", models.DateTimeField(blank=True, editable=False)),
                ("external_id", models.CharField(blank=True, max_length=50)),
                ("notes", models.TextField(blank=True)),
                ("name", models.CharField(max_length=100)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical work unit",
                "verbose_name_plural": "historical work units",
                "db_table": "work_unit_history",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="ResourcePool",
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
                ("external_id", models.CharField(blank=True, max_length=50)),
                ("notes", models.TextField(blank=True)),
                ("name", models.CharField(max_length=100)),
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
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="resource_manager.resourcepool",
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
                "db_table": "resource_pool",
            },
        ),
        migrations.CreateModel(
            name="WorkUnit",
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
                ("external_id", models.CharField(blank=True, max_length=50)),
                ("notes", models.TextField(blank=True)),
                ("name", models.CharField(max_length=100)),
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
                "db_table": "work_unit",
            },
        ),
        migrations.RemoveField(
            model_name="resourcegroup",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="resourcegroup",
            name="updated_by",
        ),
        migrations.RemoveField(
            model_name="resource",
            name="resource_groups",
        ),
        migrations.AddField(
            model_name="historicalresource",
            name="resource_type",
            field=models.CharField(
                choices=[("M", "Machine"), ("O", "Operator")], default="O", max_length=1
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resource",
            name="resource_type",
            field=models.CharField(
                choices=[("M", "Machine"), ("O", "Operator")], default="O", max_length=1
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="HistoricalResourceGroup",
        ),
        migrations.DeleteModel(
            name="ResourceGroup",
        ),
        migrations.AddField(
            model_name="resourcepool",
            name="work_units",
            field=models.ManyToManyField(
                related_name="resource_pools", to="resource_manager.workunit"
            ),
        ),
        migrations.AddField(
            model_name="historicalresourcepool",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="resource_manager.resourcepool",
            ),
        ),
        migrations.AddField(
            model_name="historicalresourcepool",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="resource_pools",
            field=models.ManyToManyField(
                related_name="resources", to="resource_manager.resourcepool"
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="work_units",
            field=models.ManyToManyField(
                related_name="resources", to="resource_manager.workunit"
            ),
        ),
    ]
