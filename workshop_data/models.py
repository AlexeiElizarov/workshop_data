from django.db import models
from django.contrib.auth.models import AbstractUser
from sign.models import User

class Order(models.Model):
    '''Класс описывает Наряд'''

    class Month(models.IntegerChoices):
        JANUARY = 1, ('январь')
        FEBRUARY = 2, ('февраль')
        MARCH = 3, ('март')
        APRIL = 4, ('апрель')
        MAY = 5, ('май')
        JUNE = 6, ('июнь')
        JULY = 7, ('июль')
        AUGUST = 8, ('август')
        SEPTEMBER = 9, ('сентябрь')
        OCTOBER = 10, ('октябрь')
        NOVEMBER = 11, ('ноябрь')
        DECEMBER = 12, ('декабрь')
        NOT_SPECIFIED = 13, ('не укзан')

    date = models.DateTimeField(auto_now_add=True)
    month = models.PositiveSmallIntegerField(choices=Month.choices, default=Month.NOT_SPECIFIED, verbose_name='Месяц')
    workshop = models.PositiveSmallIntegerField(default=464)
    section = models.PositiveSmallIntegerField(default=1, blank=False)
    surname = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Рабочий')
    employee_number = models.PositiveSmallIntegerField(blank=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Изделие')
    detail = models.ForeignKey('Detail', on_delete=models.CASCADE, verbose_name='Деталь')
    operations = models.TextField(verbose_name='Операции')
    quantity = models.PositiveSmallIntegerField(default=0, blank=False, verbose_name='Колличесво')
    normalized_time = models.FloatField(default=0, blank=False, verbose_name='Нормированное время')
    price = models.FloatField(default=0, blank=False, verbose_name='Расценка')


class Product(models.Model):
    '''Класс описывает Изделие'''
    name = models.CharField(max_length=100, unique=True, blank=False, verbose_name='Изделие')

    def __str__(self):
        return f'{self.name}'


class Detail(models.Model):
    '''Класс описывет Деталь'''
    name = models.CharField(max_length=150, blank=False, verbose_name='Деталь')
    category = models.ForeignKey('CategoryDetail', on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.name}'


class CategoryDetail(models.Model):
    '''Класс описывает Категорию Детали'''
    name = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return f'{self.name}'




