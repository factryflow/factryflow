# Generated by Django 4.2.7 on 2024-03-05 22:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resource_manager", "0007_alter_historicalresource_resource_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalresource",
            name="id",
            field=models.IntegerField(blank=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalresourcepool",
            name="id",
            field=models.IntegerField(blank=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalworkunit",
            name="id",
            field=models.IntegerField(blank=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="resource",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="resourcepool",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="workunit",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
