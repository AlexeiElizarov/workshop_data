from django.db import models
from sign.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


def product_image_directory(instance, filename):
    return ''


class Detail(models.Model):
    """Класс описывает Деталь"""
    name = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name='Деталь',
        db_index=True)
    prefix = models.ForeignKey("workshop_data.Prefix", on_delete=models.PROTECT, blank=True, null=True)
    secondary_detail = models.ManyToManyField(
        "workshop_data.Detail",
        through='workshop_data.DetailDetail',
        related_name="detail_in_detail",
        through_fields=('main_detail', 'secondary_detail'), )
    image = models.ImageField(
        upload_to='images/',
        blank=True,
        default=None,
        null=True)
    category = models.ForeignKey(
        'workshop_data.CategoryDetail',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Категория')
    balance_semis_in_warehouse = models.PositiveSmallIntegerField(default=0)
    balance_intermediate_detail_in_warehouse = models.PositiveSmallIntegerField(default=0)
    parameters_for_spu = models.OneToOneField("workshop_data.ParametersDetailForSPU",
                                              on_delete=models.SET_NULL, blank=True, null=True,
                                              )
    objects = models.Manager()

    def __str__(self):
        return f'{self.prefix}.{self.name}' if self.prefix else self.name

    def __unicode__(self):
        return self.name

    def get_name_detail(self):
        if self.secondary_detail.all():
            return f'{self.name}уз'
        return f'{self.name}'

    def get_balance_in_warehouse(self):
        return self.balance_semis_in_warehouse + self.balance_intermediate_detail_in_warehouse


class Prefix(models.Model):
    """Приставка к названию Детали"""
    name = models.CharField(max_length=10, blank=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'


class ParametersDetailForSPU(models.Model):
    """Класс описывает параметры Детали на участке СПУ"""
    operations_first_side = models.TextField(
        verbose_name='Операции 1й стороны',
        blank=True, null=True)
    operations_second_side = models.TextField(
        verbose_name='Операции 2й стороны',
        blank=True, null=True)
    first_side_time = models.FloatField(
        default=1, blank=True, null=True,
        verbose_name='Время 1я сторона')
    coefficient_first_side = models.FloatField(
        default=1, blank=True, null=True, verbose_name='Коэффициент 1'
    )
    second_side_time = models.FloatField(
        default=1, blank=True, null=True,
        verbose_name='Время 2я сторона')
    coefficient_second_side = models.FloatField(
        default=1, blank=True, null=True, verbose_name='Коэффициент 2'
    )
    price = models.FloatField(
        default=0, blank=True, null=True,
        verbose_name='Расценка')
    norm = models.FloatField(
        default=0, blank=True, null=True,
        verbose_name='Норма времени'
    )
    difficultly = models.FloatField(
        default=1,
        validators=[MaxValueValidator(2), MinValueValidator(1)],
        verbose_name='Сложность'
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_parameter_detail_cpu')

    objects = models.Manager()

    def return_salary_per_minute(self):
        """Возвращает зарплату в минуту"""
        return self.price / (self.first_side_time + self.second_side_time)

    def return_salary_per_first_side(self):
        """Возвращает зарплату по 1-й стороне"""
        return round((self.first_side_time * self.coefficient_first_side * self.return_salary_per_minute()), 2)

    def return_salary_per_second_side(self):
        """Возвращает зарплату по 2-й стороне"""
        return round((self.second_side_time * self.coefficient_second_side * self.return_salary_per_minute()), 2)

    def return_salary_per_two_side(self):
        """Возвращает зарплату по 2-ум сторонам"""
        return self.return_salary_per_first_side() + self.return_salary_per_second_side()


class MillingDetailForSPU(models.Model):
    """Параметры фрезеровки для СПУ операции"""
    name = models.CharField(max_length=250, blank=True)
    time = models.FloatField(default=0, blank=True)
    norm_milling = models.FloatField(default=0, blank=True)
    price = models.FloatField(default=0, blank=True)
    operations = models.CharField(max_length=150, blank=True)
    milling_for_detail = models.ForeignKey(
        "workshop_data.Detail",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='milling_in_detail')
