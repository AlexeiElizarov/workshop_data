from django.db import models
from sign.models import User


class Comment(models.Model):
    """Класс описывает Комментарий"""
    # object_comment = models
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_comment")

    objects = models.Manager()
