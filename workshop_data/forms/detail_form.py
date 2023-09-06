from dal import autocomplete
from django import forms

from workshop_data.models import CategoryDetail
from workshop_data.models.detail import Detail, Prefix
from django.forms import ModelChoiceField


class MyModelChoicesField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name}'


class DetailCreateForm(forms.ModelForm):
    """Отображает форму добавления новой Детали и Категории к которой она относится"""
    prefix = MyModelChoicesField(
        queryset=Prefix.objects.all(),
        label='Префикс'
    )

    def __init__(self, *args, **kwargs):
        super(DetailCreateForm, self).__init__(*args, **kwargs)
        self.fields['prefix'].required = False

    class Meta:
        model = Detail
        fields = ('prefix', 'name', 'category',)

        widgets = {
            'category': autocomplete.ModelSelect2(url='data_autocomplete_category_detail'),
        }

# Не удалять = полезно!!
    # def __init__(self, *args, **kwargs):
    #     super(DetailCreateForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs = {'class': 'form-control'}

    def clean(self):
        cleaned_data = super(DetailCreateForm, self).clean()
        name = self.cleaned_data.get('name')
        if Detail.objects.filter(name=name).exists():
            raise forms.ValidationError(f"Деталь {name} уже есть в Базе Данных")
        return cleaned_data


class DetailEditForm(forms.ModelForm):
    """Отображает форму редактирования детали"""

    class Meta:
        model = Detail
        fields = ('prefix', 'name', 'category')


class AddImageInDetailForm(forms.ModelForm):
    """Отображает форму добавления Image в Деталь"""
    class Meta:
        model = Detail
        fields = ('image',)


class DetailAddDetailForm(forms.ModelForm):
    """Отображает форму добавления Детали в Деталь"""
    # detail = fields.CharField(required=False, widget=forms.Textarea())
    # detail = forms.ModelMultipleChoiceField(
    #     queryset=Detail.objects.all()
    # )
    class Meta:
        model = Detail
        fields = (
            'name',
            'secondary_detail',
        )
        widgets = {
            'secondary_detail': autocomplete.ModelSelect2Multiple(url='data_autocomplete_detail'),
        }

    def clean(self):
        cleaned_data = super(DetailAddDetailForm, self).clean()
        # detail = Detail.objects.get(id=int(self.data.get('detail')))
        # cleaned_data['detail'] = [detail,]
        return cleaned_data
