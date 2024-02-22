from django.db import models

from sign.forms import User


class Unit(models.IntegerChoices):
    UNITS = 1, "штук"
    KILOGRAM = 2, "килограмм"
    NOT_SPECIFIED = 3, "не указан"


class Warehouse(models.Model):
    """Класс описывает детали/заготовки на складе"""
    date = models.DateTimeField(auto_now_add=True)
    section = models.SmallIntegerField(default=423,
                                       verbose_name="Участок")
    detail = models.ForeignKey("workshop_data.Detail",
                               on_delete=models.DO_NOTHING,
                               related_name="in_warehouse_detail")
    product = models.ForeignKey("workshop_data.Product",
                                on_delete=models.DO_NOTHING,
                                related_name="in_warehouse_product")
    expenditures = models.PositiveSmallIntegerField(default=0, verbose_name="Расход")
    income = models.PositiveSmallIntegerField(default=0, verbose_name="Приход")
    semis = models.BooleanField(verbose_name="Заготовка")
    intermediate_detail = models.BooleanField(verbose_name="Полуфабрикат")
    cell = models.SmallIntegerField(default=0)
    employee = models.ForeignKey("sign.User",
                                 on_delete=models.PROTECT,
                                 verbose_name="Сотрудник")
    unit = models.PositiveSmallIntegerField(
        choices=Unit.choices,
        default=Unit.NOT_SPECIFIED,
        verbose_name='Единица измерения')
    # comment = models.ForeignKey(
    #     "workshop_data.WarehouseComment",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     verbose_name='Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='user_warehouse',
        blank=True, null=True)

    objects = models.Manager()


