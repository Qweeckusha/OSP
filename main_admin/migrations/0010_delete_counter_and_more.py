# Generated by Django 5.0.4 on 2024-05-13 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_admin', '0009_rename_end_time_c_analytics_end_time_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Counter',
        ),
        migrations.RenameField(
            model_name='analytics',
            old_name='records_count',
            new_name='college_counter',
        ),
        migrations.AddField(
            model_name='analytics',
            name='university_counter',
            field=models.IntegerField(default=0),
        ),
    ]
