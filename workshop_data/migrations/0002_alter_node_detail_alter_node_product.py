# Generated by Django 4.0.6 on 2023-01-21 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='detail',
            field=models.ManyToManyField(blank=True, related_name='nodes', to='workshop_data.detail'),
        ),
        migrations.AlterField(
            model_name='node',
            name='product',
            field=models.ManyToManyField(blank=True, related_name='nodes', to='workshop_data.product'),
        ),
    ]
