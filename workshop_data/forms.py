from dal import autocomplete
from django import forms
from .models import *
import calendar

# import djhacker
# djhacker.formfield(
#     Order.product,
#     forms.ModelChoiceField,
#     widget=autocomplete.ModelSelect2(url='fff')
# )


class OrderForm(forms.ModelForm):
    '''Отображает форму добавления нового Наряда'''
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
    '''Отображает форму добавления нового Изделия'''
    class Meta:
        model = Product
        fields = ('name',)


class ProductAddDetailForm(forms.ModelForm):
    '''Отображает форму добавления новой Детали в Изделие'''
    class Meta:
        model = Product
        fields = ('name',
                  'detail',)

        widgets = {
            'detail': autocomplete.ModelSelect2(url='data_autocomplete_detail'),
        }


class DetailCreateForm(forms.ModelForm):
    '''Отображает форму добавления новой Детали и Категории к которой она относится'''
    class Meta:
        model = Detail
        fields = ('name', 'category')

        widgets = {
            'category': autocomplete.ModelSelect2(url='data_autocomplete_category_detail'),
        }


class WorkshopPlanCreateForm(forms.ModelForm):
    '''Отображает форму создания нового Плана'''
    class Meta:
        model = WorkshopPlan
        # fields = ('product', 'detail', 'month', 'year')
        fields = ('__all__')

        widgets = {
            'product': autocomplete.ModelSelect2(url='data_autocomplete_product'),
            'detail': autocomplete.ModelSelect2(url='data_autocomplete_detail'),
        }

    def clean_month(self):
        month = self.cleaned_data['month']
        return month

    def clean(self):
        super(WorkshopPlanCreateForm, self).clean()
        product = self.cleaned_data.get('product')
        month = self.cleaned_data.get('month')
        detail = self.cleaned_data.get('detail')
        print(Month.choices[month][1])
        if WorkshopPlan.objects.filter(detail=detail, month=month).exists():
            raise forms.ValidationError(f"Деталь {product} {detail} уже есть в Плане на {Month.choices[month][1]}")
        return self.cleaned_data

