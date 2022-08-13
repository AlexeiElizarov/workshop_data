from dal import autocomplete
from django import forms
from .models import *

# import djhacker
# djhacker.formfield(
#     Order.product,
#     forms.ModelChoiceField,
#     widget=autocomplete.ModelSelect2(url='fff')
# )


class OrderForm(forms.ModelForm):
    class Meta:
        NUMBERS_OPERATIONS = [('i', i) for i in range(10)]

        model = Order
        fields = ('month',
                  'surname',
                  'product',
                  'detail',
                  'operations',
                  'quantity',
                  'normalized_time',
                  'price',)
        widgets = {
            'product': autocomplete.ModelSelect2(url='data_autocomplete_product'),
            'detail': autocomplete.ModelSelect2(url='data_autocomplete_detail'),
            'surname': autocomplete.ModelSelect2(url='data_autocomplete_worker'),
            'operations': forms.CheckboxSelectMultiple(
                choices=NUMBERS_OPERATIONS,)
                # attrs={'class': 'order_operations_choices'})
        }
        # help_texts = {
        #     'surname': "",
        #     'employee_number': '',
        #     'product': "sdgdsfgsdfgdsfgfdsg"
        # }


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name',)


class DetailCreateForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ('name', 'category')


