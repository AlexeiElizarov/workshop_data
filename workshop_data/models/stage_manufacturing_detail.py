from django.db import models
from workshop_data.models.stage_name import StageName


class StageManufacturingDetail(models.Model):
    '''Описывает этапы изготовления Детали(технология)'''
    detail = models.ForeignKey('workshop_data.Detail', on_delete=models.PROTECT,
                               verbose_name="Деталь", related_name='stages')
    order = models.PositiveSmallIntegerField(verbose_name="Порядок")
    name = models.CharField(max_length=3,
                            choices=StageName.choices,
                            verbose_name="Вид работы")
    operations = models.CharField(max_length=300, blank=False, verbose_name="Операции")
    normalized_time = models.FloatField(default=0, blank=False, verbose_name="Нормированное время")
    price = models.FloatField(default=0, blank=False, verbose_name="Расценка")

    def __str__(self):
        return f'{self.operations} {self.name}'