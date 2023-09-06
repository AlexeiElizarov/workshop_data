# Generated by Django 4.0.6 on 2023-05-13 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0012_stagemanufacturingdetail_devation_card_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.SmallIntegerField(default=423)),
                ('semis', models.SmallIntegerField(default=0)),
                ('intermediate_detail', models.SmallIntegerField(default=0)),
                ('unit', models.PositiveSmallIntegerField(choices=[(1, 'штуки'), (2, 'килограмм'), (3, 'не указан')], default=3, verbose_name='Единица измерения')),
            ],
        ),
        migrations.AddField(
            model_name='workshopplan',
            name='in_warehouse',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='workshop_data.warehouse', verbose_name='в кладовой'),
            preserve_default=False,
        ),
    ]
