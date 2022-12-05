# Generated by Django 4.0.6 on 2022-11-29 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0002_rename_surname_order_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stagemanufacturingdetailinwork',
            old_name='time_of_work',
            new_name='time_of_work_stage',
        ),
        migrations.AlterField(
            model_name='order',
            name='batch',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='workshop_data.batchdetailinplan', verbose_name='Партия'),
        ),
    ]
