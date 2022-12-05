from django.db import models


class Node(models.Model):
    '''Класс описывает Узел'''
    name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name='Узел'
    )
    detail = models.ManyToManyField(
        to='workshop_data.Detail',
        blank=False,
        related_name='node',
    )
    product = models.ManyToManyField(
        to='workshop_data.Product',
        blank=False,
        related_name='node'
    )

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}уз'