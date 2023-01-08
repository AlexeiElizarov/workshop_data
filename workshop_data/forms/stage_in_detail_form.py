from django import forms
from workshop_data.models.stage_manufacturing_detail import StageManufacturingDetail
from workshop_data.models.detail import Detail


class AddStageInDetailForm(forms.ModelForm):
    """Отображает форму добавления нового Этапа в Детали"""
    class Meta:
        model = StageManufacturingDetail
        fields = ('detail', 'order', 'name', 'operations', 'normalized_time', 'price')

# автозаполнение поля по переданному из CreateView pk
    def __init__(self, *args, **kwargs):
        id = kwargs.pop('pk')
        detail = Detail.objects.get(pk=id)
        super(AddStageInDetailForm, self).__init__(*args, **kwargs)
        self.fields['detail'].initial = detail
        if StageManufacturingDetail.objects.filter(detail=detail):
            self.fields['order'].initial = \
                StageManufacturingDetail.objects.filter(detail=detail).order_by('-order')[0].order + 1


class EditStageInDetailForm(forms.ModelForm):
    """Отображает форму редактирования Этапа в Детали"""
    class Meta:
        model = StageManufacturingDetail
        fields = ('__all__')
