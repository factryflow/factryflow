# Generated by Django 4.2.7 on 2024-12-04 06:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "resource_assigner",
            "0004_remove_historicaltaskresourceassigment_assigment_rule_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="assigmentrulecriteria",
            name="operator",
            field=models.CharField(
                choices=[
                    ("equals", "Equals"),
                    ("not_equals", "Not Equals"),
                    ("contains", "Contains"),
                    ("starts_with", "Starts With"),
                    ("ends_with", "Ends With"),
                    ("gt", "Greater Than"),
                    ("lt", "Less Than"),
                    ("ib", "In Between"),
                ],
                default="equals",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="historicalassigmentrulecriteria",
            name="operator",
            field=models.CharField(
                choices=[
                    ("equals", "Equals"),
                    ("not_equals", "Not Equals"),
                    ("contains", "Contains"),
                    ("starts_with", "Starts With"),
                    ("ends_with", "Ends With"),
                    ("gt", "Greater Than"),
                    ("lt", "Less Than"),
                    ("ib", "In Between"),
                ],
                default="equals",
                max_length=20,
            ),
        ),
    ]
