from django.db import models
from sign.models import User


class BatchDetailInPlan(models.Model):
    """Класс описывает партию Деталей"""
    workshopplan_detail = models.ForeignKey(
        "workshop_data.WorkshopPlan",
        on_delete=models.SET_NULL,
        null=True,
        related_name='batchs')
    detail = models.ForeignKey("Detail", on_delete=models.PROTECT,
                               related_name="batchs",
                               verbose_name="Деталь")
    quantity_in_batch = models.SmallIntegerField(default=0, verbose_name="Количество в партии")
    ready = models.BooleanField(default=False)
    sos = models.BooleanField(default=False)
    comment = models.ForeignKey("workshop_data.Comment",
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name='Комментарий'
                                )
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_batch')

    objects = models.Manager()

    class Meta:
        verbose_name = "Партия"
        verbose_name_plural = "Партии"

    def __str__(self):
        return f'{self.id}'

    def get_product(self):
        return self.detail.product.all()[0]

    def get_detail(self):
        return self.detail
