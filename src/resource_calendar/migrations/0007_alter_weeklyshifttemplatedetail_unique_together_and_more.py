# Generated by Django 4.2.7 on 2024-04-04 05:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "resource_calendar",
            "0006_historicaloperationalexceptiontype_external_id_and_more",
        ),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="weeklyshifttemplatedetail",
            unique_together={("day_of_week", "start_time", "end_time")},
        ),
        migrations.RemoveField(
            model_name="historicalweeklyshifttemplatedetail",
            name="weekly_shift_template",
        ),
        migrations.AddField(
            model_name="historicalweeklyshifttemplate",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="weeklyshifttemplate",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="weeklyshifttemplate",
            name="weekly_shift_template_details",
            field=models.ManyToManyField(
                blank=True,
                related_name="weekly_shift_template",
                to="resource_calendar.weeklyshifttemplatedetail",
            ),
        ),
        migrations.RemoveField(
            model_name="weeklyshifttemplatedetail",
            name="weekly_shift_template",
        ),
    ]
