# Generated by Django 4.0.6 on 2022-09-22 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0005_alter_workshopplan_detail_alter_workshopplan_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stagemanufacturingdetailinwork',
            name='stage_in_batch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='workshop_data.stagemanufacturingdetail'),
        ),
    ]
