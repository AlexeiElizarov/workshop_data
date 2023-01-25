from django.db import models


class Node(models.Model):
    """Класс описывает Узел"""
    name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name='Узел'
    )
    prefix = models.ForeignKey("workshop_data.Prefix", on_delete=models.PROTECT, null=True)
    node = models.ManyToManyField(
        to='workshop_data.Node',
        symmetrical=False,
        related_name='node_within_node',
        blank=True
    )
    detail = models.ManyToManyField(
        to='workshop_data.Detail',
        related_name='nodes',
        blank=True,
    )
    category = models.ForeignKey(
        "workshop_data.CategoryDetail",
        on_delete=models.PROTECT,
        blank=True
    )
    # product = models.ManyToManyField(
    #     to='workshop_data.Product',
    #     blank=True,
    #     related_name='nodes'
    # )

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}уз'
