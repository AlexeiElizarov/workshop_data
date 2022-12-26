from dal import autocomplete
from django import forms

from workshop_data.models import StatementAboutJobOverDetail


class StatementAboutJobOverDetailForm(forms.ModelForm):
    """Форма заявление на работу над Деталью и одобрено ли оно или нет"""
    class Meta:
        model = StatementAboutJobOverDetail
        fields = ('detail',)

        widgets = {
            'detail': autocomplete.ModelSelect2(url='data_autocomplete_detail'),}
