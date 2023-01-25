from django.db import models


class Product(models.Model):
    """Класс описывает Изделие"""
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name='Изделие')
    node = models.ManyToManyField(
        'workshop_data.Node',
        blank=True,
        related_name='product',
        verbose_name='Узел'
    )
    detail = models.ManyToManyField(
        'workshop_data.Detail',
        blank=True,
        related_name='product',
        verbose_name='Деталь')

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return self.name
