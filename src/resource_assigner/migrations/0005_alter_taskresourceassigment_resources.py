# Generated by Django 4.2.7 on 2024-01-08 09:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resource_manager", "0003_resourceuserrel_resource_users"),
        (
            "resource_assigner",
            "0004_alter_assigmentrulecriteria_assigment_rule_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskresourceassigment",
            name="resources",
            field=models.ManyToManyField(
                related_name="task_resource_assigments", to="resource_manager.resource"
            ),
        ),
    ]
