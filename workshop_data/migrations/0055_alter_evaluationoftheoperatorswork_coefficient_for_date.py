# Generated by Django 4.0.6 on 2023-12-22 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0054_evaluationoftheoperatorswork_coefficient_for_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluationoftheoperatorswork',
            name='coefficient_for_date',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
