from django import forms
from workshop_data.models.stage_manufacturing_detail_in_work import StageManufacturingDetailInWork
from workshop_data.models.comment import Comment
from workshop_data.services.services import get_current_user


class CreateNewStageManufacturingInWorkForm(forms.ModelForm):
    '''Форма задания(глагол) нового Этапа работы конкретной Партии Деталей'''
    comment_in_batch = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = StageManufacturingDetailInWork
        fields = ('batch', 'stage_in_batch', 'worker', 'in_work', 'time_of_work', 'comment_in_batch')
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        batch_id = kwargs.pop('batch')
        stages = kwargs.pop('stages')
        self.user = kwargs.pop('user')
        if 'last_stage_in_work' in kwargs:
            last_stage_in_work = kwargs.pop('last_stage_in_work')
            super(CreateNewStageManufacturingInWorkForm, self).__init__(*args, **kwargs)
            self.fields['stage_in_batch'].initial = last_stage_in_work.stage_in_batch
        else:
            super(CreateNewStageManufacturingInWorkForm, self).__init__(*args, **kwargs)
            self.fields['stage_in_batch'] = forms.ModelChoiceField(
                queryset=stages)
        self.fields['batch'].initial = batch_id

    def clean(self):
        batch = self.cleaned_data.get('batch')
        stage_in_batch = self.cleaned_data.get('stage_in_batch')
        comment = self.cleaned_data.pop('comment_in_batch')
        new_comment = Comment.objects.create(body=comment, author=self.user)
        self.cleaned_data.update({'comment_in_batch': new_comment})
        if StageManufacturingDetailInWork.objects.filter(
                batch_id=batch.id, stage_in_batch_id=stage_in_batch.id
        ).exists():
            raise forms.ValidationError(f"Этап {stage_in_batch} в Партии {batch} уже есть!") #FIXME реализовать проверку View
