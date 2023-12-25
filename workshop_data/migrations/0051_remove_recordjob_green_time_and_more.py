# Generated by Django 4.0.6 on 2023-12-10 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workshop_data', '0050_recordjob_green_time_recordjob_work_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recordjob',
            name='green_time',
        ),
        migrations.RemoveField(
            model_name='recordjob',
            name='work_time',
        ),
        migrations.CreateModel(
            name='EvaluationOfTheOperatorsWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('work_time', models.SmallIntegerField(default=0)),
                ('green_time', models.SmallIntegerField(default=0)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='evaluation_work', to=settings.AUTH_USER_MODEL, verbose_name='Рабочий')),
            ],
        ),
    ]
