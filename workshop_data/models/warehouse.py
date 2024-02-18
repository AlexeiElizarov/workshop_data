from django.db import models

from sign.forms import User


class Unit(models.IntegerChoices):
    UNITS = 1, "штук"
    KILOGRAM = 2, "килограмм"
    NOT_SPECIFIED = 3, "не указан"


class Warehouse(models.Model):
    """Класс описывает детали/заготовки на складе"""
    section = models.SmallIntegerField(default=423,
                                       verbose_name="Участок")
    semis = models.SmallIntegerField(
        default=0,
        verbose_name="Заготовка")
    intermediate_detail = models.SmallIntegerField(
        default=0,
        verbose_name="Полуфабрикат")
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


