# Generated by Django 4.2.7 on 2024-01-17 12:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resource_manager", "0006_historicalresourcepool_historicalworkunit_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalresource",
            name="resource_type",
            field=models.CharField(
                blank=True,
                choices=[("M", "Machine"), ("O", "Operator")],
                max_length=1,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="resource",
            name="resource_type",
            field=models.CharField(
                blank=True,
                choices=[("M", "Machine"), ("O", "Operator")],
                max_length=1,
                null=True,
            ),
        ),
    ]
