# Generated by Django 4.2.7 on 2024-04-02 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("job_manager", "0008_alter_job_dependencies_item"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicaltask",
            name="item",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="job_manager.item",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="item",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="tasks",
                to="job_manager.item",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="task",
            name="task_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks_type",
                to="job_manager.tasktype",
            ),
        ),
    ]
