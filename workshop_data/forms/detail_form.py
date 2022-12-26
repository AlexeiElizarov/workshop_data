from dal import autocomplete
from django import forms
from workshop_data.models.detail import Detail


class DetailCreateForm(forms.ModelForm):
    """Отображает форму добавления новой Детали и Категории к которой она относится"""
    class Meta:
        model = Detail
        fields = ('name', 'category')

        widgets = {
            'category': autocomplete.ModelSelect2(url='data_autocomplete_category_detail'),
        }

    def clean(self):
        name = self.cleaned_data.get('name')
        if Detail.objects.filter(name=name).exists():
            raise forms.ValidationError(f"Деталь {name} уже есть в Базе Данных")


class AddImageInDetailForm(forms.ModelForm):
    """Отображает форму добавления Image в Деталь"""
    class Meta:
        model = Detail
        fields = ('image',)
