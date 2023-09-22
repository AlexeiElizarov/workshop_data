
import django_filters
from django import forms

from django_filters import FilterSet, filters
from django_filters.widgets import RangeWidget

from sign.models import User
from workshop_data.models import Bonus, Order, RecordJob
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
        queryset=Detail.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_detail')
    )

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
        widget= forms.DateInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Order
        fields = ('date', )


class WorkersFilter(FilterSet):
    """Фильтр поиска Детали"""
    surname = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_worker')
    )

    class Meta:
        model = User
        fields = ['surname']


class RecordJobFilter(FilterSet):
    """Фильтр поиска записи выполненных работ на участке СПУ"""
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_product')
    )
    detail = django_filters.ModelChoiceFilter(
        queryset=Detail.objects.all().select_related('prefix', ),
        widget=autocomplete.Select2(url='data_autocomplete_detail')
    )

    # month = django_filters.MultipleChoiceFilter(
    #     choices=Month.choices,
    #     widget=forms.CheckboxSelectMultiple()
    # )
    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_worker_cpu')
    )
    # month = django_filters.MultipleChoiceFilter(
    #     choices=Month.choices,
    #     widget=forms.RadioSelect)

    class Meta:
        model = RecordJob
        fields = ['product', 'detail', 'month', 'user']

