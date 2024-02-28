import django_filters
from django import forms

from django_filters import FilterSet, filters
from django_filters.widgets import RangeWidget

from sign.models import User
from workshop_data.models import Bonus, Order, RecordJob, Warehouse
from workshop_data.models.product import Product
from workshop_data.models.detail import Detail
from workshop_data.models.workshop_plan import WorkshopPlan
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from dal import autocomplete
from workshop_data.models.month import Month


class ProductFilter(FilterSet):
    """Фильр поиска Изделия"""
    name = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_product')
    )

    class Meta:
        model = Product
        fields = ['name']


class DetailFilter(FilterSet):
    """Фильтр поиска Детали"""
    name = django_filters.ModelChoiceFilter(
        queryset=Detail.objects.all().select_related('prefix'),
        widget=autocomplete.Select2(url='data_autocomplete_detail'),
        method='name_filter'
    )

    def name_filter(self, qs, name, value):
        # if value.prefix:
        #     return qs.filter(**{name: value.name})

        return qs.filter(**{name: value.name})

    class Meta:
        model = Detail
        fields = ['name']


class WorkshopPlanFilter(FilterSet):
    """Фильтр поиска Изделия по Плану"""
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_product')
    )
    detail = django_filters.ModelChoiceFilter(
        queryset=Detail.objects.all().select_related('prefix', ),
        widget=autocomplete.Select2(url='data_autocomplete_detail')
    )
    month = django_filters.MultipleChoiceFilter(
        choices=Month.choices,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = WorkshopPlan
        fields = ['product', 'detail', 'month']


class BatchFilter(FilterSet):
    """Фильтр поиска Партии"""
    id = django_filters.ModelChoiceFilter(
        label='Номер Партии',
        queryset=BatchDetailInPlan.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_batch'),
        method='filter_id'
    )

    def filter_id(self, queryset, name, value):
        return queryset.filter(id=value.id)

    class Meta:
        model = BatchDetailInPlan
        fields = ['id']


class BonusFilter(FilterSet):
    """Фильтр поиска Премии по месяцу"""
    month = django_filters.MultipleChoiceFilter(
        choices=Month.choices,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Bonus
        fields = ['month']


class OrdersFilter(FilterSet):
    """Фильтр поиска наряда по дате"""
    date = django_filters.DateFilter(
        field_name='date',
        label=('Дата'),
        input_formats=["%d.%m.%Y"],
        lookup_expr='contains',
        widget=forms.DateInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Order
        fields = ('date',)


class WorkersFilter(FilterSet):
    """Фильтр поиска Детали"""
    surname = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_worker')
    )

    class Meta:
        model = User
        fields = ['surname']


FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]


class RecordJobFilter(FilterSet):
    """Фильтр поиска записи выполненных работ на участке СПУ"""
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_product')
    )
    detail = django_filters.ModelChoiceFilter(
        queryset=Detail.objects.all().select_related('prefix', ),
        widget=autocomplete.Select2(url='data_autocomplete_detail'),
        field_name='detail',
    )

    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_worker_cpu')
    )
    month = django_filters.MultipleChoiceFilter(
        choices=Month.choices,
        widget=forms.CheckboxSelectMultiple(),
        field_name='month',
    )
    milling = django_filters.BooleanFilter(
        label='С фрезеровкой',
        field_name='milling_in_detail__name',
        lookup_expr='contains',
        )
    milling_was = django_filters.BooleanFilter(
        label='С фрезеровкой',
        widget=forms.CheckboxInput,
        method='filter_milling',
    )

    class Meta:
        model = RecordJob
        fields = ['product', 'detail', 'month', 'user', 'milling', 'milling_was']

    def filter_milling(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(**{name: value})


class WarehouseRecordsFilter(FilterSet):
    """Фильтр поиска записи в кладовой"""
    employee = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_worker')
    )
    class Meta:
        model = Warehouse
        fields = ['employee',]
