# Generated by Django 4.2.7 on 2024-05-05 20:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("resource_assigner", "0013_remove_assignmentconstraint_work_units"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assignmentconstraint",
            name="required_units",
        ),
    ]