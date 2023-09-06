from django.db import models
from workshop_data.models.stage_name import StageName


class StageManufacturingDetail(models.Model):
    """Описывает этапы изготовления Детали(технология)"""
    detail = models.ForeignKey('workshop_data.Detail', on_delete=models.PROTECT,
                               verbose_name="Деталь", related_name='stages_detail',
                               blank=True, null=True)
    order = models.PositiveSmallIntegerField(verbose_name="Порядок")
    description = models.CharField(max_length=150, verbose_name='Описание')
    name = models.CharField(max_length=3,
                            choices=StageName.choices,
                            verbose_name="Вид работы")
    operations = models.CharField(max_length=300, blank=False, verbose_name="Операции")
    class_work = models.CharField(max_length=20, blank=True, verbose_name='Разряд работы')
    normalized_time = models.FloatField(default=0, blank=False, verbose_name="Нормированное время")
    price = models.FloatField(default=0, blank=False, verbose_name="Расценка")
    devation_card = models.CharField(max_length=30, blank=True, verbose_name='Карта отклонения')

    objects = models.Manager()

    def __str__(self):
        return f'{self.operations} {self.description}'

    def get_operations(self):
        return self.operations

    def get_name_work(self):
        return f'{self.get_name_display()}'


