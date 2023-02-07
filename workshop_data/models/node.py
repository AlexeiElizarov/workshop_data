# from django.db import models
#
#
# class Node(models.Model):
#     """Класс описывает Узел"""
#     name = models.CharField(
#         max_length=100,
#         blank=False,
#         verbose_name='Узел'
#     )
#     prefix = models.ForeignKey("workshop_data.Prefix", on_delete=models.PROTECT, null=True)
#
#     node = models.ManyToManyField(
#         "workshop_data.Node",
#         through='workshop_data.NodeNode',
#         related_name="nodes_in_node",
#         through_fields=('node2', 'node'),)
#     detail = models.ManyToManyField(
#         "workshop_data.Detail",
#         through='workshop_data.NodeDetail',
#         related_name="details_in_node",
#         through_fields=('node', 'detail'),)
#
#     # node = models.ManyToManyField(
#     #     to='workshop_data.Node',
#     #     symmetrical=False,
#     #     related_name='node_within_node',
#     #     blank=True
#     # )
#     # detail = models.ManyToManyField(
#     #     to='workshop_data.Detail',
#     #     related_name='nodes',
#     #     blank=True,
#     # )
#     category = models.ForeignKey(
#         "workshop_data.CategoryDetail",
#         on_delete=models.PROTECT,
#         blank=True,
#         null=True
#     )
#
#     objects = models.Manager()
#
#     def __str__(self):
#         return f'{self.name}уз'
