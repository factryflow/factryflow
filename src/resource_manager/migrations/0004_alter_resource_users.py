# Generated by Django 4.2.7 on 2024-01-11 11:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("resource_manager", "0003_resource_users"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="users",
            field=models.ManyToManyField(
                related_name="operators", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]