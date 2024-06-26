# Generated by Django 4.2.7 on 2024-03-05 22:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resource_manager", "0008_alter_historicalresource_id_and_more"),
        ("resource_assigner", "0009_alter_assignmentconstraint_resources_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assignmentconstraint",
            name="resources",
            field=models.ManyToManyField(
                blank=True, related_name="constraints", to="resource_manager.resource"
            ),
        ),
        migrations.AlterField(
            model_name="assignmentconstraint",
            name="work_units",
            field=models.ManyToManyField(
                blank=True, related_name="constraints", to="resource_manager.workunit"
            ),
        ),
    ]
