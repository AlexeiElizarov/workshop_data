# Generated by Django 4.0.6 on 2022-09-11 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0003_workshopplan_in_work_alter_workshopplan_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchdetailinplan',
            name='detail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workshop_data.workshopplan'),
        ),
    ]
