# Generated by Django 4.0.6 on 2023-03-22 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0005_alter_detail_prefix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='batch',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='workshop_data.batchdetailinplan', verbose_name='Партия'),
        ),
    ]
