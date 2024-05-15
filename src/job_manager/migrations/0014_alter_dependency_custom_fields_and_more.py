# Generated by Django 4.2.7 on 2024-05-15 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_manager", "0013_alter_dependency_custom_fields_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dependency",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="dependencytype",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldependency",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldependencytype",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="historicalitem",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="historicaljob",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="historicaljobtype",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="historicaltask",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="historicaltasktype",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="historicalworkcenter",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="item",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="jobtype",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="tasktype",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="workcenter",
            name="custom_fields",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
