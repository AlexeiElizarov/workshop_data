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


class StageName(models.TextChoices):
    EMPTY_VALUE = '', ('Выберите вид работы')
    LOCKSMITH = 'LSM', ('Слесарый')
    TURNER = 'TRN', ('Токарный')
    MILLER = 'MLR', ('Фрезеровальный')
    GRINDER = 'GRN', ('Шлифовальный')




class WorkshopPlan(models.Model):
    #FIXME
    '''Класс описывает Детали входящие в План цеха'''

    product = models.ForeignKey("Product", on_delete=models.PROTECT, verbose_name='_Изделие_')
    detail = models.ForeignKey("Detail", on_delete=models.PROTECT)
    # quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Колличество')
    quantity_state_order = models.PositiveSmallIntegerField(default=0, verbose_name='Госзаказ')
    quantity_commercial_order = models.PositiveSmallIntegerField(default=0, verbose_name='Коммерция')

    in_work = models.PositiveSmallIntegerField(default=0, verbose_name='Колличество в работе')
    month = models.PositiveSmallIntegerField(choices=Month.choices, default=Month.NOT_SPECIFIED, verbose_name='_Месяц_')
    sos = models.BooleanField(default=False)
    year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(2022), max_value_current_year])

    def __str__(self):
        return f'{self.product}_{self.detail}'

    def get_product(self):
        return f'{self.product} {self.detail}'

    def get_quantity(self):
        quantity = self.quantity_state_order + self.quantity_commercial_order
        return quantity

    def get_quantity_for_all_batch(self):
        '''Возвращает количество деталей во всех партиях self'''
        obj = BatchDetailInPlan.objects.filter(workshopplan_detail_id=self.id)
        count = sum([batch.quantity_in_batch for batch in obj])
        return count


class Comment(models.Model):
    '''Класс описывает Комментарий'''
    body = models.TextField()


class Order(models.Model):
    '''Класс описывает Наряд'''
    date = models.DateTimeField(auto_now_add=True)
    month = models.PositiveSmallIntegerField(choices=Month.choices, default=Month.NOT_SPECIFIED, verbose_name='Месяц')
    workshop = models.PositiveSmallIntegerField(default=464)
    section = models.PositiveSmallIntegerField(default=1, blank=False)
    surname = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Рабочий')
    employee_number = models.PositiveSmallIntegerField(blank=False)
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='Изделие')
    detail = models.ForeignKey('Detail', on_delete=models.PROTECT, verbose_name='Деталь')
    operations = models.TextField(verbose_name='Операции')
    quantity = models.PositiveSmallIntegerField(default=0, blank=False, verbose_name='Количество')
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
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Категория')

    def __str__(self):
        return f'{self.name}'


class StageManufacturingDetail(models.Model):
    '''Описывает этапы изготовления Детали(технология)'''
    detail = models.ForeignKey('Detail', on_delete=models.PROTECT,
                               verbose_name="Деталь", related_name='stages')
    order = models.PositiveSmallIntegerField(verbose_name="Порядок")
    name = models.CharField(max_length=3,
                            choices=StageName.choices,
                            verbose_name="Вид работы")
    operations = models.CharField(max_length=300, blank=False, verbose_name="Операции")
    normalized_time = models.FloatField(default=0, blank=False, verbose_name="Нормированное время")
    price = models.FloatField(default=0, blank=False, verbose_name="Расценка")

    def __str__(self):
        return f'{self.operations} {self.name}'


class BatchDetailInPlan(models.Model):
    '''Класс описывает партию Деталей'''
    workshopplan_detail = models.ForeignKey("WorkshopPlan", on_delete=models.SET_NULL,
                                            null=True, related_name='batchs')
    quantity_in_batch = models.SmallIntegerField(default=0, verbose_name="Колличество в партии")
    ready = models.BooleanField(default=False)
    sos = models.BooleanField(default=False)
    comment = models.ForeignKey("Comment",
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name='Комментарий'
                                )

    def __str__(self):
        return f'{self.id}'

class StageManufacturingDetailInWork(models.Model):
    '''Описывает этап изготовления Детали(в Плане)'''
    batch = models.ForeignKey(
        "BatchDetailInPlan",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Партия',
        related_name='stages')
    worker = models.ForeignKey\
        (User,
         on_delete=models.SET_NULL,
         null=True,
         verbose_name='Рабочий')
    stage_in_batch = models.ForeignKey(
        "StageManufacturingDetail",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Этап')
    start_of_work = models.DateTimeField(auto_now_add=True)
    in_work = models.BooleanField(default=True, verbose_name='В работе')
    time_of_work = models.SmallIntegerField(default=0, blank=True, verbose_name='Время')
    comment_in_batch = models.ForeignKey(
        "Comment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Комментарий') #FIXME


class CategoryDetail(models.Model):
    '''Класс описывает Категорию Детали'''
    name = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return f'{self.name}'
