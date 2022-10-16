# Generated by Django 4.0.6 on 2022-10-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0002_alter_user_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(choices=[('LSM', 'Слесарь'), ('TRN', 'Токарь'), ('MLR', 'Фрезеровщик'), ('MSR', 'Мастер'), ('EPB', 'Инженер ПДБ')], max_length=3),
        ),
    ]
