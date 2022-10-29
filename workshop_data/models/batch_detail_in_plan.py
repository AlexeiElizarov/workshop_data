from django.db import models


class BatchDetailInPlan(models.Model):
    '''Класс описывает партию Деталей'''
    workshopplan_detail = models.ForeignKey(
        "workshop_data.WorkshopPlan",
        on_delete=models.SET_NULL,
        null=True,
        related_name='batchs')
    quantity_in_batch = models.SmallIntegerField(default=0, verbose_name="Колличество в партии")
    ready = models.BooleanField(default=False)
    sos = models.BooleanField(default=False)
    comment = models.ForeignKey("workshop_data.Comment",
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name='Комментарий'
                                )

    class Meta:
        verbose_name = "Партия"
        verbose_name_plural = "Партии"

    def __str__(self):
        return f'{self.id}'