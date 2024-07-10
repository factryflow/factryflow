# Generated by Django 4.2.7 on 2024-06-24 10:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resource_calendar", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="weeklyshifttemplate",
            name="weekly_shift_template_details",
            field=models.ManyToManyField(
                blank=True,
                related_name="weekly_shift_template",
                to="resource_calendar.weeklyshifttemplatedetail",
            ),
        ),
    ]
