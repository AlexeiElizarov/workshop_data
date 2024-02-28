from django.db import models

from sign.forms import User


class Unit(models.IntegerChoices):
    UNITS = 1, "шт."
    KILOGRAM = 2, "кг."
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
    balance_semis_on_this_moment = models.PositiveSmallIntegerField(default=0)
    intermediate_detail = models.BooleanField(verbose_name="Полуфабрикат")
    balance_intermediate_detail_on_this_moment = models.PositiveSmallIntegerField(default=0)
    balance_in_warehouse_on_this_moment = models.PositiveSmallIntegerField(default=0)
    cell = models.SmallIntegerField(default=0)
    employee = models.ForeignKey("sign.User",
                                 on_delete=models.PROTECT,
                                 verbose_name="Сотрудник")
    unit = models.PositiveSmallIntegerField(
        choices=Unit.choices,
        default=Unit.NOT_SPECIFIED,
        verbose_name='Единица измерения')
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='user_warehouse',
        blank=True, null=True)

    objects = models.Manager()

    # def save(self, *args, **kwargs):
    #     self.balance_in_warehouse_on_this_moment = self.detail.get_balance_on_this_moment() + self.income - self.expenditures ####
    #     if self.semis:
    #         self.balance_semis_on_this_moment += self.detail.balance_semis_in_warehouse + self.income - self.expenditures
    #         self.balance_intermediate_detail_on_this_moment = self.detail.balance_intermediate_detail_in_warehouse
    #         self.detail.balance_semis_in_warehouse += self.income - self.expenditures
    #     elif self.intermediate_detail:
    #         self.balance_intermediate_detail_on_this_moment += self.detail.balance_intermediate_detail_in_warehouse + self.income - self.expenditures
    #         self.balance_semis_on_this_moment = self.detail.balance_semis_in_warehouse
    #         self.detail.balance_intermediate_detail_in_warehouse += self.income - self.expenditures
    #     self.detail.save()
    #     super(Warehouse, self).save(*args, **kwargs)

