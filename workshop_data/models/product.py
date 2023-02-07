from django.db import models


class Product(models.Model):
    """Класс описывает Изделие"""
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name='Изделие')

    detail = models.ManyToManyField(
        "workshop_data.Detail",
        through='workshop_data.ProductDetail',
        related_name="detail_in_product",
        through_fields=('product', 'detail'),)


    # node = models.ManyToManyField(
    #     "workshop_data.Node",
    #     through='workshop_data.ProductNode',
    #     related_name="node_in_product",
    #     through_fields=('product', 'node'),)

    # node = models.ManyToManyField(
    #     'workshop_data.Node',
    #     blank=True,
    #     related_name='product',
    #     verbose_name='Узел'
    # )
    # detail = models.ManyToManyField(
    #     'workshop_data.Detail',
    #     blank=True,
    #     related_name='product',
    #     verbose_name='Деталь')

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return self.name


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


# class ProductNode(models.Model):
#     """Таблица связи Изделия и Узла"""
#     product = models.ForeignKey("workshop_data.Product", on_delete=models.PROTECT)
#     node = models.ForeignKey("workshop_data.Node", on_delete=models.PROTECT)
#     quantity = models.SmallIntegerField(default=1)

# class NodeDetail(models.Model):
#     """Таблица связи Узла и Детали"""
#     node = models.ForeignKey("workshop_data.Node", on_delete=models.PROTECT)
#     detail = models.ForeignKey("workshop_data.Detail", on_delete=models.PROTECT)
#     quantity = models.SmallIntegerField(default=1)


# class NodeNode(models.Model):
#     """Таблица связи Узла и Детали"""
#     node = models.ForeignKey(
#         "workshop_data.Node",
#         on_delete=models.PROTECT,
#         related_name="nodes")
#     node2 = models.ForeignKey(
#         "workshop_data.Node",
#         on_delete=models.PROTECT,
#         related_name="nodes2")
#     quantity = models.SmallIntegerField(default=1)