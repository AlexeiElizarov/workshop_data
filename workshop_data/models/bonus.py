from django.db import models
from sign.models import User
from workshop_data.models import Month
from workshop_data.models.comment import Comment

class Bonus(models.Model):
    """Класс описывает модель Премии(Bonus) выписываемой работнику мастером или начальником"""
    worker = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=False,
        verbose_name="Работник",
        related_name="user_bonus")
    quantity = models.SmallIntegerField(default=0, verbose_name="Сумма")
    month = models.PositiveSmallIntegerField(
        choices=Month.choices,
        default=Month.NOT_SPECIFIED,
        verbose_name='Месяц')
    time = models.SmallIntegerField(default=0, verbose_name="Затраченное время")
    # comment = models.ForeignKey(
    #     Comment,
    #     on_delete=models.PROTECT,
    #     blank=False,
    #     verbose_name="Комментарий")
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=False,
        verbose_name="Автор",
        related_name="author_bonus")

    objects = models.Manager()

    def __str__(self):
        return f'Премия {self.pk}'