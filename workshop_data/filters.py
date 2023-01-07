import django_filters
from django import forms
from django_filters import FilterSet

from workshop_data.models import Bonus
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
        queryset=Detail.objects.all(),
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

