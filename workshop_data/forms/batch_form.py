from django import forms
from workshop_data.models.workshop_plan import WorkshopPlan
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from workshop_data.models.detail import Detail
from workshop_data.models.comment import Comment, BatchComment


class CreateBatchDetailInPlanForm(forms.ModelForm):
    """Отображает форму создания новой Партии Деталей"""
    comment = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = BatchDetailInPlan
        fields = ['quantity_in_batch', 'sos', 'comment']

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('object')
        self.user = kwargs.pop('user')
        # detail = name.split('_')[1]
        super(CreateBatchDetailInPlanForm, self).__init__(*args, **kwargs)
        # вот так показывает "LSM", "TRN"...
        # self.fields['stage'].queryset = StageManufacturingDetail.objects.filter(detail_id=detail_id)

        # self.fields['stage'] = forms.ChoiceField(
        #         choices=StageManufacturingDetail.objects.filter(detail_id=detail_id))

        # self.fields['stage'] = forms.ModelChoiceField(
        #     queryset=StageManufacturingDetail.objects.filter(detail_id=detail_id))
        # self.fields['stage'].label = 'Выберите вид работы' #FIXME

    def clean(self):
        comment = self.cleaned_data.pop('comment')
        new_comment = BatchComment.objects.create(body=comment, author=self.user)
        self.cleaned_data.update({'comment': new_comment})
