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
        default=0, blank=True,
        verbose_name='Количество по 1й стороне')
    quantity_2 = models.PositiveSmallIntegerField(
        default=0, blank=True,
        verbose_name='Количество по 2й стороне')
    quantity = models.PositiveSmallIntegerField(
        default=0, blank=True,
         verbose_name='Количество по двум сторонам')
    milling_was = models.BooleanField(default=False, blank=True, null=True)
    order_yes = models.BooleanField(default=False,
                                    verbose_name='Наряд выписан')
    order_at_master = models.BooleanField(default=False,
                                    verbose_name='Наряд сдан')

    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='record_job_spy')
    objects = models.Manager()


    def __str__(self):
        return f'{self.product} {self.detail}'


# class RecordJob2(models.Model):
#     """Класс описывает запись сделанной работы в БД"""
#     class Machine(models.TextChoices):
#         SMEC_1 = '001', 'Смек 1'
#         SMEC_2 = '002', 'Смек 2 барфидер'
#         SMEC_3 = '003', 'Смек 3'
#         SMEC_4 = '004', 'Смек 4 барфидер'
#         SPINNER_1 = '005', 'Шпинер 1'
#         SPINNER_2 = '006', 'Шпинер 2'
#         HI5000 = '007', 'Малыш'
#
#
#     date = models.DateField(auto_now_add=True)
#     month = models.PositiveSmallIntegerField(
#         choices=Month.choices,
#         default=Month.NOT_SPECIFIED,
#         verbose_name='Месяц')
#     user = models.ForeignKey(
#         User,
#         on_delete=models.PROTECT,
#         verbose_name='Рабочий',
#         related_name="records_job")
#     product = models.ForeignKey(
#         'workshop_data.Product',
#         on_delete=models.PROTECT,
#         verbose_name='Изделие')
#     detail = models.ForeignKey(
#         'workshop_data.Detail',
#         on_delete=models.PROTECT,
#         verbose_name='Деталь')
#     quantity_1 = models.PositiveSmallIntegerField(
#         default=0, blank=True,
#         verbose_name='Количество по 1й стороне')
#     quantity_2 = models.PositiveSmallIntegerField(
#         default=0, blank=True,
#         verbose_name='Количество по 2й стороне')
#     quantity = models.PositiveSmallIntegerField(
#         default=0, blank=True,
#          verbose_name='Количество по двум сторонам')
#     milling_was = models.BooleanField(default=False, blank=True, null=True)
#     order_yes = models.BooleanField(default=False,
#                                     verbose_name='Наряд выписан')
#     order_at_master = models.BooleanField(default=False,
#                                     verbose_name='Наряд сдан')
#
#     machine = models.CharField(max_length=3, choices=Machine.choices, verbose_name='Станок')
#     work_time_green = models.FloatField(default=0, null=True, blank=True)
#     barfider = models.BooleanField(default=False)
#     author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='record_job_spy')
#
#     objects = models.Manager()
#
#
#     def __str__(self):
#         return f'{self.product} {self.detail}'