from dal import autocomplete
from django import forms
from django.forms import Select, NumberInput

from workshop_data.models import Month, Comment
from workshop_data.models.workshop_plan import WorkshopPlan
from workshop_data.services import current_year


class WorkshopPlanCreateForm(forms.ModelForm):
    """Отображает форму создания нового Плана"""
    comment = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control",
            # 'placeholder':'Комментарий',
            'rows': 4,
            'cols': 5}
    ))
    month = forms.ChoiceField(choices=Month.choices,
                              label='Месяц',
                              initial=Month.NOT_SPECIFIED,
                              widget=Select(
                                  attrs={"class": "form-control"},
                              ))
    quantity_state_order = forms.DecimalField(
        label='Госзаказ',
        required=False,
        widget=NumberInput(
            attrs={"class": "form-control"}, ))
    quantity_commercial_order = forms.DecimalField(
        label='Коммерция',
        required=False,
        widget=NumberInput(
            attrs={"class": "form-control"}, ))
    year = forms.DecimalField(
        label='Год',
        initial=current_year(),
        widget=NumberInput(
            attrs={"class": "form-control"},))


    class Meta:
        model = WorkshopPlan
        fields = '__all__'
        exclude = ('author', 'in_work',)
        widgets = {
            'product': autocomplete.ModelSelect2(url='data_autocomplete_product'),
            'detail': autocomplete.ModelSelect2(url='data_autocomplete_detail'),
            # 'node': autocomplete.ModelSelect2(url='data_autocomplete_node'),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(WorkshopPlanCreateForm, self).__init__(*args, **kwargs)

    def clean_month(self):
        month = self.cleaned_data['month']
        return month

    def clean(self):
        comment = self.cleaned_data.pop('comment')
        new_comment = Comment.objects.create(body=comment, author=self.user)
        self.cleaned_data.update({'comment': new_comment})
        super(WorkshopPlanCreateForm, self).clean()
        product = self.cleaned_data.get('product')
        month = self.cleaned_data.get('month')
        detail = self.cleaned_data.get('detail')
        if WorkshopPlan.objects.filter(detail=detail, month=month).exclude(detail=None).exists():
            raise forms.ValidationError(f"Деталь {product} {detail} уже есть в Плане на {Month.choices[int(month) - 1][1]}")
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
