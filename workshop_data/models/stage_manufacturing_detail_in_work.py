from django.db import models
from sign.models import User


class StageManufacturingDetailInWork(models.Model):
    '''Описывает этап изготовления Детали(в Плане)'''
    batch = models.ForeignKey(
        "workshop_data.BatchDetailInPlan",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Партия',
        related_name='stages')
    worker = models.ForeignKey\
        (User,
         on_delete=models.SET_NULL,
         null=True,
         verbose_name='Рабочий')
    stage_in_batch = models.ForeignKey(
        "workshop_data.StageManufacturingDetail",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Этап')
    start_of_work = models.DateTimeField(auto_now_add=True)
    in_work = models.BooleanField(default=True, verbose_name='В работе')
    time_of_work = models.SmallIntegerField(default=0, blank=True, verbose_name='Время')
    job_is_done = models.BooleanField(default=False)
    comment_in_batch = models.ForeignKey(
        "workshop_data.Comment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Комментарий') #FIXME
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_stage_in_work')
