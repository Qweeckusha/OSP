# Generated by Django 5.0.4 on 2024-05-12 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_admin', '0005_alter_adminuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='called',
            field=models.BooleanField(default=False),
        ),
    ]