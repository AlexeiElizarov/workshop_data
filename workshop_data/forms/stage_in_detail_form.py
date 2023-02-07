from django import forms

from workshop_data.models.stage_manufacturing_detail import StageManufacturingDetail
from workshop_data.models.detail import Detail


class AddStageInDetailForm(forms.ModelForm):
    """Отображает форму добавления нового Этапа в Детали"""
    class Meta:
        model = StageManufacturingDetail
        fields = ('detail', 'order', 'description', 'name', 'operations', 'normalized_time', 'price')

# автозаполнение поля по переданному из CreateView pk
    def __init__(self, *args, **kwargs):
        if 'detail_id' in kwargs:
            detail = Detail.objects.get(pk=kwargs.pop('detail_id'))
            super(AddStageInDetailForm, self).__init__(*args, **kwargs)
            self.fields['detail'].initial = detail
            if StageManufacturingDetail.objects.filter(detail=detail):
                self.fields['order'].initial = \
                    StageManufacturingDetail.objects.filter(detail=detail).order_by('-order')[0].order + 1
        elif 'node_id' in kwargs:
            node = Node.objects.get(pk=kwargs.pop('node_id'))
            super(AddStageInDetailForm, self).__init__(*args, **kwargs)
            self.fields['node'].initial = node
            if StageManufacturingDetail.objects.filter(node=node):
                self.fields['order'].initial = \
                    StageManufacturingDetail.objects.filter(node=node).order_by('-order')[0].order + 1





class EditStageInDetailForm(forms.ModelForm):
    """Отображает форму редактирования Этапа в Детали"""
    class Meta:
        model = StageManufacturingDetail
        fields = ('__all__')
