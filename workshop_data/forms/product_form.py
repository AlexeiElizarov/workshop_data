from dal import autocomplete
from django import forms

from workshop_data.models import Detail
from workshop_data.models.product import Product


class ProductCreateForm(forms.ModelForm):
    """Отображает форму добавления нового Изделия"""
    class Meta:
        model = Product
        fields = ('name',)

    def clean(self):
        name = self.cleaned_data.get('name')
        if Product.objects.filter(name=name).exists():
            raise forms.ValidationError(f"Изделие {name} уже есть в Базе Данных")


class ProductAddDetailForm(forms.ModelForm):
    """Отображает форму добавления новой Детали в Изделие"""
    name = forms.CharField(label="Изделие")
    detail = forms.ModelChoiceField(
        label="Деталь",
        widget=autocomplete.ModelSelect2(url='data_autocomplete_detail'),
        queryset=Detail.objects.all()
    )
    class Meta:
        model = Product
        fields = ['name', 'detail']
        # widgets = {
        #     'detail': autocomplete.ModelSelect2(url='data_autocomplete_detail'),
        # }

    def clean(self):
        cleaned_data = super(ProductAddDetailForm, self).clean()
        name = self.cleaned_data.get('name')
        detail = Detail.objects.get(id=self.data.get('detail'))
        if Product.objects.filter(name=name, detail=detail).exists():
            raise forms.ValidationError(f"Деталь {detail} уже есть в Изделие {name}")
        return cleaned_data

    def clean_detail(self):
        data = self.cleaned_data.get('detail')
