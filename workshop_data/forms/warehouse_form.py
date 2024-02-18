from django import forms
from django.forms import NumberInput, Select

from workshop_data.models import Warehouse, WarehouseComment, Unit


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
    semis = forms.DecimalField(
        label='Заготовка',
        required=True,
        widget=NumberInput(
            attrs={"class": "form-control"}, ))
    intermediate_detail = forms.DecimalField(
        label='Полуфабрикат',
        required=True,
        widget=NumberInput(
            attrs={"class": "form-control"}, ))
    unit = forms.ChoiceField(choices=Unit.choices,
                              label='Еденица измерения',
                              initial=Unit.NOT_SPECIFIED,
                              widget=Select(
                                  attrs={"class": "form-control"},
                              ))


    class Meta:
        model = Warehouse
        fields = ['section', 'semis', 'intermediate_detail', 'unit', 'comment']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(WarehouseCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        comment = self.cleaned_data.pop('comment')
        new_comment = WarehouseComment.objects.create(body=comment, author=self.user)
        self.cleaned_data.update({'comment': new_comment})
