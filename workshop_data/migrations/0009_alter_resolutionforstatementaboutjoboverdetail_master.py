# Generated by Django 4.0.6 on 2022-12-20 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workshop_data', '0008_remove_resolutionforstatementaboutjoboverdetail_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resolutionforstatementaboutjoboverdetail',
            name='master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Мастер'),
        ),
    ]
