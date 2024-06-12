# Generated by Django 4.2.7 on 2024-05-23 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("resource_manager", "0017_alter_historicalresource_custom_fields_and_more"),
        ("resource_assigner", "0021_remove_assigmentrule_resource_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="taskresourceassigment",
            name="resource",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="resource_manager.resource",
            ),
        ),
    ]