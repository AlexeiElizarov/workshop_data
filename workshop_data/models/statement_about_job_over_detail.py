from django.db import models
from sign.models import User
from workshop_data.models import Detail


class StatementAboutJobOverDetail(models.Model):
    """Класс описывает заявление на работу над Деталью"""
    detail = models.ForeignKey(Detail, on_delete=models.PROTECT, verbose_name="Деталь")
    worker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Рабочий")
    date_statement = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Заявление {self.worker} о детали {self.detail}"


class ResolutionForStatementAboutJobOverDetail(models.Model):
    """Разрешение на заявление на работу над Деталью"""
    statement = models.ForeignKey(StatementAboutJobOverDetail, on_delete=models.PROTECT, related_name="resolute")
    master = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Мастер")
    resolution = models.BooleanField(default=False)
    date_approval = models.DateTimeField(default=None, blank=True, null=True)

    objects = models.Manager()

