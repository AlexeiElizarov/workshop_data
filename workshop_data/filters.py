import django_filters
from django import forms
from django_filters import FilterSet
from workshop_data.models.product import Product
from workshop_data.models.detail import Detail
from workshop_data.models.workshop_plan import WorkshopPlan
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from dal import autocomplete
from workshop_data.models.month import Month

class ProductFilter(FilterSet):
    name = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_product')
        )
    class Meta:
        model = Product
        fields = ['name']


class DetailFilter(FilterSet):
    name = django_filters.ModelChoiceFilter(
        queryset=Detail.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_detail')
        )
    class Meta:
        model = Detail
        fields = ['name']


class WorkshopPlanFilter(FilterSet):
    '''Фильтр поиска Изделия по Плану'''
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_product')
        )
    month = django_filters.MultipleChoiceFilter(
        choices=Month.choices,
        widget=forms.CheckboxSelectMultiple()

    )
    class Meta:
        model = WorkshopPlan
        fields = ['product', 'month']



class BatchFilter(FilterSet):
    '''Фильтр поиска Партии'''
    id = django_filters.ModelChoiceFilter(
        queryset=BatchDetailInPlan.objects.all(),
        widget=autocomplete.Select2(url='data_autocomplete_batch')
    )
    class Meta:
        model = BatchDetailInPlan
        fields = ['id']



