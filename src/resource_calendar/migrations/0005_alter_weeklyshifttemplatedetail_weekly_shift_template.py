# Generated by Django 4.2.7 on 2023-12-18 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "resource_calendar",
            "0004_alter_historicaloperationalexception_external_id_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="weeklyshifttemplatedetail",
            name="weekly_shift_template",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="details",
                to="resource_calendar.weeklyshifttemplate",
            ),
        ),
    ]
