# Generated by Django 4.0.6 on 2023-12-12 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0052_evaluationoftheoperatorswork_barfider_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationoftheoperatorswork',
            name='coefficient',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
