# Generated by Django 4.2.7 on 2024-01-18 14:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("issue", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="active",
        ),
        migrations.RemoveField(
            model_name="historicalcomment",
            name="active",
        ),
    ]