# Generated by Django 5.0.4 on 2024-05-13 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_admin', '0008_analytics_time_c_analytics_time_u'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analytics',
            old_name='end_time_c',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='analytics',
            old_name='quantity_college',
            new_name='records_count',
        ),
        migrations.RenameField(
            model_name='analytics',
            old_name='start_time_c',
            new_name='start_time',
        ),
        migrations.RemoveField(
            model_name='analytics',
            name='end_time_u',
        ),
        migrations.RemoveField(
            model_name='analytics',
            name='quantity_main',
        ),
        migrations.RemoveField(
            model_name='analytics',
            name='quantity_university',
        ),
        migrations.RemoveField(
            model_name='analytics',
            name='start_time_u',
        ),
        migrations.RemoveField(
            model_name='analytics',
            name='time_c',
        ),
        migrations.RemoveField(
            model_name='analytics',
            name='time_u',
        ),
        migrations.AddField(
            model_name='analytics',
            name='processing_duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='analytics',
            name='processing_status',
            field=models.BooleanField(default=False),
        ),
    ]
