from django.db import models

class Detail(models.Model):
    '''Класс описывет Деталь'''
    name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Деталь')
    category = models.ForeignKey(
        'workshop_data.CategoryDetail',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Категория')

    def __str__(self):
        return f'{self.name}'