# Generated by Django 4.0.6 on 2023-10-12 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0042_millingdetailforspu_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordjob',
            name='milling_was',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
