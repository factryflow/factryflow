# Generated by Django 4.2.7 on 2024-05-06 09:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "resource_assigner",
            "0015_rename_resource_pool_assignmentconstraint_resource_group",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="taskresourceassigment",
            old_name="resource_pool",
            new_name="resource_group",
        ),
    ]
