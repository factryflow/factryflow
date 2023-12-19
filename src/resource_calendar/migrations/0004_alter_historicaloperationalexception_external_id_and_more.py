# Generated by Django 4.2.7 on 2023-12-18 12:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "resource_calendar",
            "0003_weeklyshifttemplatedetail_weekly_shif_day_of__a7f991_idx",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicaloperationalexception",
            name="external_id",
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name="historicaloperationalexception",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="historicalweeklyshifttemplate",
            name="name",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name="operationalexception",
            name="external_id",
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name="operationalexception",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="weeklyshifttemplate",
            name="name",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterUniqueTogether(
            name="weeklyshifttemplatedetail",
            unique_together={
                ("day_of_week", "weekly_shift_template", "start_time", "end_time")
            },
        ),
    ]