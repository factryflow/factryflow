# Generated by Django 4.2.7 on 2024-10-29 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("job_manager", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicaltask",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="job_manager.task",
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sub_tasks",
                to="job_manager.task",
            ),
        ),
    ]
