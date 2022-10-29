from django.db import models


class Comment(models.Model):
    '''Класс описывает Комментарий'''
    body = models.TextField()