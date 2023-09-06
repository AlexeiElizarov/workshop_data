# Generated by Django 4.0.6 on 2023-08-24 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0032_parametersdetailforspu_norm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametersdetailforspu',
            name='first_side_time',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Время 1я сторона'),
        ),
        migrations.AlterField(
            model_name='parametersdetailforspu',
            name='second_side_time',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Время 2я сторона'),
        ),
    ]
