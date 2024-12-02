# Generated by Django 4.2.7 on 2024-11-22 08:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("job_manager", "0002_historicaltask_parent_task_parent"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="job",
            options={"ordering": ["priority", "due_date"]},
        ),
        migrations.AddField(
            model_name="historicaljob",
            name="manual_priority",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="job",
            name="manual_priority",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="historicaljob",
            name="priority",
            field=models.IntegerField(default=None, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="priority",
            field=models.IntegerField(default=None, editable=False, null=True),
        ),
        migrations.AlterModelTable(
            name="job",
            table=None,
        ),
    ]