# Generated by Django 4.0.6 on 2022-07-30 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(choices=[('LSM', 'Слесарь'), ('TRN', 'Токарь'), ('MLR', 'Фрезеровщик'), ('MSR', 'Мастер')], max_length=3),
        ),
    ]
