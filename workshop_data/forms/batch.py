from django import forms
from workshop_data.models.workshop_plan import WorkshopPlan
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from workshop_data.models.detail import Detail
from workshop_data.models.comment import Comment


class CreateBatchDetailInPlanForm(forms.ModelForm):
    '''Отображает форму создания новой Партии Деталей'''
    comment = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
    workshopplan_detail = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=WorkshopPlan.objects.all()
    )
    class Meta:
        model = BatchDetailInPlan
        fields = ['workshopplan_detail', 'quantity_in_batch', 'sos', 'comment']

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('object')
        detail = name.split('_')[1]
        detail_id = Detail.objects.get(name=f'{detail}').id
        detail_in_plan = WorkshopPlan.objects.get(detail_id=detail_id)
        super(CreateBatchDetailInPlanForm, self).__init__(*args, **kwargs)
        self.fields['workshopplan_detail'].label = 'Деталь'
        self.fields['workshopplan_detail'].initial = detail_in_plan
        # вот так показывает "LSM", "TRN"...
        # self.fields['stage'].queryset = StageManufacturingDetail.objects.filter(detail_id=detail_id)

        # self.fields['stage'] = forms.ChoiceField(
        #         choices=StageManufacturingDetail.objects.filter(detail_id=detail_id))

        # self.fields['stage'] = forms.ModelChoiceField(
        #     queryset=StageManufacturingDetail.objects.filter(detail_id=detail_id))
        # self.fields['stage'].label = 'Выберите вид работы' #FIXME

    def clean(self):
        comment = self.cleaned_data.pop('comment')
        new_comment = Comment.objects.create(body=comment)
        self.cleaned_data.update({'comment': new_comment})
