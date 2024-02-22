from django.db import models
from sign.models import User


class Comment(models.Model):
    """Класс описывает Комментарий"""
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True


class WorkshopPlanComment(Comment):
    workshop_plan = models.ForeignKey("workshop_data.WorkshopPlan",
                                      on_delete=models.SET_NULL,
                                      null=True)
    objects = models.Manager()


class BatchComment(Comment):
    batch_detail_in_plan = models.ForeignKey("workshop_data.BatchDetailInPlan",
                                      on_delete=models.SET_NULL,
                                      null=True)
    objects = models.Manager()


class WarehouseComment(Comment):
    warehouse = models.ForeignKey("workshop_data.Warehouse",
                                  on_delete=models.SET_NULL,
                                  null=True)
    objects = models.Manager()


class BonusComment(Comment):
    bonus = models.ForeignKey("workshop_data.WorkshopPlan",
                                      on_delete=models.SET_NULL,
                                      null=True)
    objects = models.Manager()


class StageManufacturingDetailInWorkComment(Comment):
    bonus = models.ForeignKey("workshop_data.WorkshopPlan",
                                      on_delete=models.SET_NULL,
                                      null=True)
    objects = models.Manager()
