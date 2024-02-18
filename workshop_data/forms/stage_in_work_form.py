from dal import autocomplete
from django import forms

from sign.forms import User
from workshop_data.models import BatchDetailInPlan, StageManufacturingDetail, Detail
from workshop_data.models.stage_manufacturing_detail_in_work import StageManufacturingDetailInWork
from workshop_data.models.comment import Comment, StageManufacturingDetailInWorkComment
from workshop_data.services.general_services import get_list_all_workers, get_list_all_workers_initials
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class InitialsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class CreateNewStageManufacturingInWorkForm(forms.ModelForm):
    """Форма задания(глагол) нового Этапа работы конкретной Партии Деталей"""
    comment_in_batch = forms.CharField(widget=forms.Textarea,
                                       label="Комментарий")

    class Meta:
        model = StageManufacturingDetailInWork
        fields = ('batch', 'stage_in_batch', 'worker', 'in_work', 'comment_in_batch')#, 'time_of_work_stage'
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
                queryset=stages, label='Этап производста')
        self.fields['batch'].initial = batch_id
        self.fields['worker'] = InitialsModelChoiceField(
            queryset=User.objects.all(),
            label='Рабочий',
            widget=autocomplete.ModelSelect2(url='data_autocomplete_worker'))

    def clean(self):
        cleaned_data = super().clean()
        comment = cleaned_data.pop('comment_in_batch')
        new_comment = StageManufacturingDetailInWorkComment.objects.create(body=comment, author=self.user)
        cleaned_data.update({'comment_in_batch': new_comment})
        worker = self.cleaned_data['worker']
        stage_in_batch = self.cleaned_data['stage_in_batch']
        batch = self.cleaned_data['batch']

        # список типа [1, 2, 3] где 1,2,3 номера этапов
        stage_exists_list = [i.stage_in_batch.order for i in StageManufacturingDetailInWork.objects.filter(batch=batch)]

        # список типа [<StageManufacturingDetail: 10,20,30 LSM>,
        # <StageManufacturingDetail: 40,50 MLR>]
        stage_in_batch_list = [i.stage_in_batch for i in
                               StageManufacturingDetailInWork.objects.filter(batch=self.cleaned_data['batch'])]

        if stage_in_batch in stage_in_batch_list:
            raise ValidationError(_("Такой этап уже есть в партии"))
        if not StageManufacturingDetailInWork.objects.filter(batch=batch).exists() and stage_in_batch.order != 1:
            raise forms.ValidationError(f"Не пройдены предыдущие этапы в Партии {batch}!")

        if stage_exists_list:
            if stage_in_batch.order - 1 != sorted(stage_exists_list)[-1]:
                raise forms.ValidationError(
                    f"Не пройдены предыдущие этапы в Партии {batch}")
        # if worker.position != stage_in_batch.name:
        #     raise forms.ValidationError(
        #         f"Вы пытаетесь выписать наряд на {stage_in_batch.name} рабочему {worker.position}")
        return cleaned_data


class EnteringDetailToViewAverageTimeOfWorkForm(forms.ModelForm):
    """Форма ввода Изделия Детали для отображения среднего времени работы"""
    quantity_detail = forms.IntegerField()
    class Meta:
        model = Detail
        fields = ('name', 'quantity_detail')
        # fields = '__all__'








