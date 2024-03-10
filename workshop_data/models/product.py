from django.db import models
from django.shortcuts import reverse


class Product(models.Model):
    """Класс описывает Изделие"""
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name='Изделие')
        
    order_number_commercial = models.SmallIntegerField(blank=True, verbose_name='Коммерция')
    order_number_state = models.SmallIntegerField(blank=True, verbose_name='Г/з')
    slug = models.SlugField(max_length=50, blank=True, unique=True)
    detail = models.ManyToManyField(
        "workshop_data.Detail",
        through='workshop_data.ProductDetail',
        related_name="detail_in_product",
        through_fields=('product', 'detail'),)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail_data', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.name
        super().save(*args, **kwargs)


class ProductDetail(models.Model):
    """Таблица связи Изделия и Детали"""
    product = models.ForeignKey("workshop_data.Product", on_delete=models.PROTECT)
    detail = models.ForeignKey("workshop_data.Detail", on_delete=models.PROTECT)
    quantity = models.SmallIntegerField(default=1)


class DetailDetail(models.Model):
    """Таблица связи Детали и Детали"""
    main_detail = models.ForeignKey("workshop_data.Detail",
                                    on_delete=models.PROTECT)
    secondary_detail = models.ForeignKey("workshop_data.Detail",
                                         on_delete=models.PROTECT,
                                         related_name="secondary_detail_in_main")
    quantity = models.SmallIntegerField(default=1)
