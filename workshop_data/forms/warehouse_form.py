from dal import autocomplete
from django import forms
from django.forms import NumberInput, Select

from sign.forms import User
from workshop_data.models import Warehouse, WarehouseComment, Unit, Product, Detail


class WarehouseCreateForm(forms.ModelForm):
    """"""
    comment = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control",
                   # 'placeholder':'Комментарий',
                   'rows': 4,
                   'cols': 5}
        ))
    section = forms.DecimalField(
        label='Участок',
        required=True,
        initial=423,
        widget=NumberInput(
            attrs={"class": "form-control"}, ))
    product = forms.ModelChoiceField(
        label='Изделие',
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='data_autocomplete_product',
                                         forward=('detail',))
    )
    detail = forms.ModelChoiceField(
        queryset=Detail.objects.all(),
        label="Деталь",
        widget=autocomplete.ModelSelect2(url='data_autocomplete_detail_for_product',
                                         forward=('product',))
    )
    employee = forms.ModelChoiceField(
        label='Сотрудник',
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='data_autocomplete_worker_cpu')
    )
    income = forms.DecimalField(
        label='Приход',
        widget=NumberInput(
            attrs={"class": "form-control"}, ))
    expenditures = forms.DecimalField(
        label='Расход',
        widget=NumberInput(
            attrs={"class": "form-control"}, ))
    semis = forms.BooleanField(label='Заготовка', required=False)
    intermediate_detail = forms.BooleanField(label='Полуфабрикат', required=False)
    cell = forms.IntegerField(
            label='Ячейка',
            widget=NumberInput(
                attrs={"class": "form-control"}, ))
    unit = forms.ChoiceField(choices=Unit.choices,
                              label='Ед. изм.',
                              initial=Unit.NOT_SPECIFIED,
                              widget=Select(
                                  attrs={"class": "form-control"},
                              ))

    class Meta:
        prefix="form1"
        model = Warehouse
        fields = ['section', 'product', 'detail', 'employee', 'income', 'expenditures', 'semis', 'intermediate_detail', 'cell', 'unit', 'comment']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        product = kwargs.pop('product', None)
        detail = kwargs.pop('detail', None)
        super(WarehouseCreateForm, self).__init__(*args, **kwargs)
        if product:
            self.fields['product'].initial = product
        if detail:
            self.fields['detail'].initial = detail
        self.fields['income'].initial = 0
        self.fields['expenditures'].initial = 0

    def clean(self):
        comment = self.cleaned_data.pop('comment')
        if comment:
            new_comment = WarehouseComment.objects.create(body=comment, author=self.user)
            self.cleaned_data.update({'comment': new_comment})

        semis = self.cleaned_data.get('semis')
        intermediate_detail = self.cleaned_data.get('intermediate_detail')
        if (semis and intermediate_detail) or (not semis and not intermediate_detail):
            raise forms.ValidationError('Выберите или "Заготовка", или "Полуфабрикат"')

        income = self.cleaned_data.get('income')
        expenditures = self.cleaned_data.get('expenditures')
        if (income > 0 and expenditures) or (income == 0 and expenditures == 0) > 0:
            raise forms.ValidationError('Заполните "Приход", или "Расход"')


class ViewWarehouseRecordForm(forms.Form):
    product = forms.ModelChoiceField(
        label='Изделие',
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='data_autocomplete_product',
                                         forward=('detail',))
    )
    detail = forms.ModelChoiceField(
        queryset=Detail.objects.all(),
        label="Деталь",
        widget=autocomplete.ModelSelect2(url='data_autocomplete_detail_for_product',
                                         forward=('product',))
    )
