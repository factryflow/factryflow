# Generated by Django 4.2.7 on 2024-03-14 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("resource_manager", "0009_remove_resource_resource_pools_and_more"),
        ("resource_assigner", "0010_alter_assignmentconstraint_resources_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="taskresourceassigment",
            name="resource",
        ),
        migrations.AddField(
            model_name="taskresourceassigment",
            name="assigment_rule",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="resource_assigner.assigmentrule",
            ),
        ),
        migrations.AddField(
            model_name="taskresourceassigment",
            name="resource_count",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="taskresourceassigment",
            name="resource_pool",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="resource_manager.resourcepool",
            ),
        ),
        migrations.AddField(
            model_name="taskresourceassigment",
            name="use_all_resources",
            field=models.BooleanField(default=False),
        ),
    ]
