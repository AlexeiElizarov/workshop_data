# Generated by Django 4.0.6 on 2022-10-10 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0018_workshopplan_ready'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopplan',
            name='ready',
        ),
        migrations.AddField(
            model_name='batchdetailinplan',
            name='ready',
            field=models.BooleanField(default=False),
        ),
    ]
