from dal import autocomplete
from django import forms
from workshop_data.models.detail import Detail

class DetailCreateForm(forms.ModelForm):
    '''Отображает форму добавления новой Детали и Категории к которой она относится'''
    class Meta:
        model = Detail
        fields = ('name', 'category')

        widgets = {
            'category': autocomplete.ModelSelect2(url='data_autocomplete_category_detail'),
        }
