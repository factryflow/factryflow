# Generated by Django 4.2.7 on 2024-05-23 05:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("resource_assigner", "0020_assigmentrule_resource_assigmentrule_task"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assigmentrule",
            name="resource",
        ),
        migrations.RemoveField(
            model_name="assigmentrule",
            name="task",
        ),
    ]