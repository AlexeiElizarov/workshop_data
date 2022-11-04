from dal import autocomplete
from django import forms
from workshop_data.models.product import Product


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
