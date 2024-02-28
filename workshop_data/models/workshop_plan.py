from django.core.validators import MinValueValidator
from django.db import models
from workshop_data.models.month import Month
from workshop_data.services import current_year, max_value_current_year
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from sign.models import User


class WorkshopPlan(models.Model):
    """Класс описывает Детали входящие в План цеха"""
    product = models.ForeignKey("workshop_data.Product",
                                on_delete=models.PROTECT,
                                verbose_name='Изделие')
    detail = models.ForeignKey("workshop_data.Detail",
                               on_delete=models.PROTECT,
                               verbose_name="Деталь",
                               blank=True,
                               null=True)
    quantity_state_order = models.PositiveSmallIntegerField(default=0, verbose_name='Госзаказ')
    quantity_commercial_order = models.PositiveSmallIntegerField(default=0, verbose_name='Коммерция')
    in_work = models.PositiveSmallIntegerField(default=0, verbose_name='Количество в работе')
    month = models.PositiveSmallIntegerField(choices=Month.choices,
                                             default=Month.NOT_SPECIFIED,
                                             verbose_name='Месяц')
    sos = models.BooleanField(default=False)
    year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(2022), max_value_current_year])
    # comment = models.ForeignKey("workshop_data.Comment",
    #                             blank=True,
    #                             on_delete=models.PROTECT,
    #                             verbose_name='Заметки')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_workshopplan')

    objects = models.Manager()

    def __str__(self):
        return f'{self.product}_{self.detail}'

    def get_product(self):
        return f'{self.product} {self.detail}'

    def get_quantity(self):
        """Возвращает общее количество деталей(госзаказ и коммерция)"""
        quantity = self.quantity_state_order + self.quantity_commercial_order
        return quantity

    def get_quantity_for_all_batch(self):
        """Возвращает количество деталей во всех партиях self"""
        obj = BatchDetailInPlan.objects.filter(workshopplan_detail_id=self.id)
        count = sum([batch.quantity_in_batch for batch in obj])
        return count
