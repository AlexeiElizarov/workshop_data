from django.db import models
from django.contrib.auth.models import AbstractUser
from sign.models import User
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

def current_year():
    return datetime.date.today().year

def current_month():
    return datetime.date.today().month

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

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


class WorkshopPlan(models.Model):
    '''Класс описывает План цеха'''
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    detail = models.ForeignKey("Detail", on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=0, verbose_name='Колличество')
    month = models.PositiveSmallIntegerField(choices=Month.choices, default=Month.NOT_SPECIFIED, verbose_name='_Месяц_')
    sos = models.BooleanField(default=False)
    year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(2022), max_value_current_year])

    def __str__(self):
        return f'{self.product}'

    def get_product(self):
        return f'{self.product} {self.detail}'

# class ProductInPlan(models.Model):
#     '''Класс описывает Изделие входящее в план'''
#     name = models.OneToOneField("Product", on_delete=models.CASCADE, verbose_name='_Изделие_')
#     details = models.ForeignKey('DetailInPlan', on_delete=models.CASCADE, related_name='product')
#
#
# class DetailInPlan(models.Model):
#     '''Класс описывает Детеаль входящую в план'''
#     name = models.OneToOneField("Detail", on_delete=models.CASCADE, verbose_name='_Деталь_')
#     quantity = models.SmallIntegerField(default=0, verbose_name='Колличество')
#     quantity_batch = models.SmallIntegerField(default=1, verbose_name='_Партия_')
#     sos = models.BooleanField(default=False)
#     batch = models.ForeignKey("BatchDetailInPlan", on_delete=models.CASCADE, related_name='detail_in_plan')


class BatchDetailInPlan(models.Model):
    '''Класс описывает партию Деталей'''
    worker = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Рабочий')
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, verbose_name='Комментарий')


class Comment(models.Model):
    '''Класс описывает Комментарий'''
    body = models.TextField()



class Order(models.Model):
    '''Класс описывает Наряд'''
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
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name='Изделие')
    detail = models.ManyToManyField(
        'Detail',
        blank=True,
        related_name='product',
        verbose_name='Деталь')

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return self.name


class Node(models.Model):
    '''Класс описывает Узел'''
    name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name='Узел'
    )
    detail = models.ManyToManyField(
        'Detail',
        blank=False,
        related_name='node',
    )
    product = models.ManyToManyField(
        'Product',
        blank=False,
        related_name='node'
    )

    def __str__(self):
        return f'{self.name}уз'


class Detail(models.Model):
    '''Класс описывет Деталь'''
    name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Деталь')
    category = models.ForeignKey(
        'CategoryDetail',
        on_delete=models.CASCADE,
        verbose_name='Категория')

    def __str__(self):
        return f'{self.name}'


class CategoryDetail(models.Model):
    '''Класс описывает Категорию Детали'''
    name = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return f'{self.name}'




