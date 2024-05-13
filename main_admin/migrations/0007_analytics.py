# Generated by Django 5.0.4 on 2024-05-13 09:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_admin', '0006_customuser_called'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time_u', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time_u', models.DateTimeField(blank=True, null=True)),
                ('start_time_c', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time_c', models.DateTimeField(blank=True, null=True)),
                ('quantity_main', models.IntegerField(default=0)),
                ('quantity_college', models.IntegerField(default=0)),
                ('quantity_university', models.IntegerField(default=0)),
            ],
        ),
    ]
