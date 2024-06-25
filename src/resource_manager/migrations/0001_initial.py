# Generated by Django 4.2.7 on 2024-06-24 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('custom_fields', models.JSONField(blank=True, default=dict, null=True)),
                ('external_id', models.CharField(blank=True, max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('resource_type', models.CharField(choices=[('Machine', 'Machine'), ('Operator', 'Operator')], default='Operator', max_length=9)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, related_name='operators', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'resource',
            },
        ),
        migrations.CreateModel(
            name='ResourceGroup',
            fields=[
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('custom_fields', models.JSONField(blank=True, default=dict, null=True)),
                ('external_id', models.CharField(blank=True, max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='resource_manager.resourcegroup')),
                ('resources', models.ManyToManyField(related_name='related_resources', to='resource_manager.resource')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'resource_pool',
            },
        ),
        migrations.CreateModel(
            name='HistoricalResourceGroup',
            fields=[
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('custom_fields', models.JSONField(blank=True, default=dict, null=True)),
                ('external_id', models.CharField(blank=True, max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('name', models.CharField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='resource_manager.resourcegroup')),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical resource group',
                'verbose_name_plural': 'historical resource groups',
                'db_table': 'resource_grp_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalResource',
            fields=[
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('custom_fields', models.JSONField(blank=True, default=dict, null=True)),
                ('external_id', models.CharField(blank=True, max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('name', models.CharField(max_length=100)),
                ('resource_type', models.CharField(choices=[('Machine', 'Machine'), ('Operator', 'Operator')], default='Operator', max_length=9)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical resource',
                'verbose_name_plural': 'historical resources',
                'db_table': 'resource_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
