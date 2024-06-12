# Generated by Django 4.2.7 on 2024-03-20 09:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("resource_manager", "0009_remove_resource_resource_pools_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="users",
            field=models.ManyToManyField(
                blank=True, related_name="operators", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="resource",
            name="work_units",
            field=models.ManyToManyField(
                blank=True, related_name="resources", to="resource_manager.workunit"
            ),
        ),
    ]