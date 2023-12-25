# Generated by Django 4.0.6 on 2023-10-15 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_data', '0046_millingdetailforspu_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='millingdetailforspu',
            name='author',
        ),
        migrations.RemoveField(
            model_name='millingdetailforspu',
            name='comment',
        ),
        migrations.AddField(
            model_name='millingdetailforspu',
            name='name',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
