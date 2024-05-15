# Generated by Django 4.2.7 on 2024-04-02 05:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customfield",
            name="field_type",
            field=models.CharField(
                choices=[
                    ("text", "Text"),
                    ("integer", "Integer"),
                    ("date", "Date"),
                    ("time", "Time"),
                    ("datetime", "Datetime"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="historicalcustomfield",
            name="field_type",
            field=models.CharField(
                choices=[
                    ("text", "Text"),
                    ("integer", "Integer"),
                    ("date", "Date"),
                    ("time", "Time"),
                    ("datetime", "Datetime"),
                ],
                max_length=10,
            ),
        ),
    ]
