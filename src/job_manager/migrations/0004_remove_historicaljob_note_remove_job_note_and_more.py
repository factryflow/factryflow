# Generated by Django 4.2.7 on 2024-01-14 09:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "job_manager",
            "0003_alter_dependency_external_id_alter_dependency_notes_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicaljob",
            name="note",
        ),
        migrations.RemoveField(
            model_name="job",
            name="note",
        ),
        migrations.AddField(
            model_name="dependencytype",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="dependencytype",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="historicaldependencytype",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="historicaldependencytype",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="historicaljob",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="historicaljobtype",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="historicaljobtype",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="historicaltask",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="historicaltasktype",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="historicaltasktype",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="historicalworkcenter",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="job",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="jobtype",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="jobtype",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="task",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="tasktype",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="tasktype",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="workcenter",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="dependency",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="historicaldependency",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="historicaljob",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="historicaltask",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="historicalworkcenter",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="task",
            name="external_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="workcenter",
            name="notes",
            field=models.TextField(blank=True),
        ),
    ]
