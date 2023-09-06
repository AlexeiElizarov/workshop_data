from django.db import models
from workshop_data.models.month import Month
from sign.models import User


class RecordJob(models.Model):
    """Класс описывает запись сделанной работы в БД"""
    date = models.DateField(auto_now_add=True)
    month = models.PositiveSmallIntegerField(
        choices=Month.choices,
        default=Month.NOT_SPECIFIED,
        verbose_name='Месяц')
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Рабочий',
        related_name="records_job")
    product = models.ForeignKey(
        'workshop_data.Product',
        on_delete=models.PROTECT,
        verbose_name='Изделие')
    detail = models.ForeignKey(
        'workshop_data.Detail',
        on_delete=models.PROTECT,
        verbose_name='Деталь')
    quantity_1 = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True,
        verbose_name='Количество по 1й стороне')
    quantity_2 = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True,
        verbose_name='Количество по 2й стороне')
    quantity = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True,
        verbose_name='Количество по двум сторонам')

    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='record_job_spy')
    objects = models.Manager()



