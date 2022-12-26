from django.db import models
from sign.models import User

class CategoryDetail(models.Model):
    '''Класс описывает Категорию Детали'''
    name = models.CharField(max_length=50, unique=True, blank=False, verbose_name="Название")
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'
    