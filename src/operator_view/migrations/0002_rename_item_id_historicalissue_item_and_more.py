# Generated by Django 4.2.7 on 2024-01-08 13:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("operator_view", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalissue",
            old_name="item_id",
            new_name="item",
        ),
        migrations.RenameField(
            model_name="historicalissue",
            old_name="task_id",
            new_name="task",
        ),
        migrations.RenameField(
            model_name="issue",
            old_name="item_id",
            new_name="item",
        ),
        migrations.RenameField(
            model_name="issue",
            old_name="task_id",
            new_name="task",
        ),
    ]
