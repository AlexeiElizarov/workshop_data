# Generated by Django 4.0.6 on 2023-02-20 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0002_order_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='operations',
            field=models.TextField(blank=True, verbose_name='Операции'),
        ),
    ]
