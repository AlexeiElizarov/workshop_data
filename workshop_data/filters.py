import django_filters
from django_filters import FilterSet
from .models import *
from dal import autocomplete

class ProductFilter(FilterSet):
    name = django_filters.ModelChoiceFilter(queryset=Product.objects.all(),
                                            widget=autocomplete.Select2(url='data_autocomplete_product')
                                            )
    class Meta:
        model = Product
        fields = ['name']


class DetailFilter(FilterSet):
    name = django_filters.ModelChoiceFilter(queryset=Detail.objects.all(),
                                            widget=autocomplete.Select2(url='data_autocomplete_detail')
                                            )
    class Meta:
        model = Detail
        fields = ['name']