from dal import autocomplete
from django import forms

from workshop_data.models import Month
from workshop_data.models.workshop_plan import WorkshopPlan


class WorkshopPlanCreateForm(forms.ModelForm):
    """Отображает форму создания нового Плана"""

    class Meta:
        model = WorkshopPlan
        fields = '__all__'
        exclude = ('author', 'in_work',)
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
        if WorkshopPlan.objects.filter(detail=detail, month=month).exists():
            raise forms.ValidationError(f"Деталь {product} {detail} уже есть в Плане на {Month.choices[month][1]}")
        return self.cleaned_data


class EditWorkshopPlanForm(forms.ModelForm):
    """Отображает форму редактирования Детали в Плане"""
    class Meta:
        model = WorkshopPlan
        fields = '__all__'


class WorkshopPlanAddExistingBatchForm(forms.ModelForm):
    """Форма добавления существующей партии в план"""
    batch = forms.IntegerField(
        label='Номер существующей партии'
    )
    class Meta:
        model = WorkshopPlan
        fields = ('product', 'detail',)
