from django.db import models


def product_image_directory(instance, filename):
    return ''


class Detail(models.Model):
    """Класс описывает Деталь"""
    name = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name='Деталь',
        db_index=True)
    prefix = models.ForeignKey("workshop_data.Prefix", on_delete=models.PROTECT, null=True)
    image = models.ImageField(
        upload_to='images/',
        blank=True,
        default=None,
        null=True)
    category = models.ForeignKey(
        'workshop_data.CategoryDetail',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Категория')

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'


class Prefix(models.Model):
    """Приставка к названию Детали"""
    #FIXME
    name = models.CharField(max_length=10, blank=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'
