from django.db import models


class Product(models.Model):
    '''Класс описывает Изделие'''
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name='Изделие')
    detail = models.ManyToManyField(
        'workshop_data.Detail',
        blank=True,
        related_name='product',
        verbose_name='Деталь')

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return self.name