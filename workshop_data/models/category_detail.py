from django.db import models

class CategoryDetail(models.Model):
    '''Класс описывает Категорию Детали'''
    name = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return f'{self.name}'