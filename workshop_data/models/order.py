from django.db import models
from workshop_data.models.month import Month
from sign.models import User

class Order(models.Model):
    '''Класс описывает Наряд'''
    date = models.DateTimeField(auto_now_add=True)
    month = models.PositiveSmallIntegerField(choices=Month.choices, default=Month.NOT_SPECIFIED, verbose_name='Месяц')
    workshop = models.PositiveSmallIntegerField(default=464)
    section = models.PositiveSmallIntegerField(default=1, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Рабочий')
    employee_number = models.PositiveSmallIntegerField(blank=False)
    product = models.ForeignKey('workshop_data.Product', on_delete=models.PROTECT, verbose_name='Изделие')
    detail = models.ForeignKey('workshop_data.Detail', on_delete=models.PROTECT, verbose_name='Деталь')
    batch = models.ForeignKey('workshop_data.BatchDetailInPlan',
                              default=1, null=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Партия')
    operations = models.TextField(verbose_name='Операции')
    quantity = models.PositiveSmallIntegerField(default=0, blank=False, verbose_name='Количество')
    normalized_time = models.FloatField(default=0, blank=False, verbose_name='Нормированное время')
    price = models.FloatField(default=0, blank=False, verbose_name='Расценка')
    time_of_work_order = models.SmallIntegerField(default=0, blank=True, verbose_name='Затраченное время')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_order')

    objects = models.Manager()

    def get_clean_operations(self):
        """Получает операции без приставки профессии"""
        return self.operations.operations


