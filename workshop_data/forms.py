from dal import autocomplete
from django import forms
from .models import *
import calendar

# import djhacker
# djhacker.formfield(
#     Order.product,
#     forms.ModelChoiceField,
#     widget=autocomplete.ModelSelect2(url='fff')
# )


class OrderForm(forms.ModelForm):
    '''Отображает форму добавления нового Наряда'''
    class Meta:
        NUMBERS_OPERATIONS = [('i', i) for i in range(10)]

        model = Order
        fields = ('month',
                  'surname',
                  'product',
                  'detail',
                  'operations',
                  'quantity',
                  'normalized_time',
                  'price',)
        widgets = {
            'product': autocomplete.ModelSelect2(url='data_autocomplete_product'),
            'detail': autocomplete.ModelSelect2(url='data_autocomplete_detail'),
            'surname': autocomplete.ModelSelect2(url='data_autocomplete_worker'),
            # 'operations': forms.ModelChoiceField(
            #     choices=NUMBERS_OPERATIONS,)
                # attrs={'class': 'order_operations_choices'})
        }
        # help_texts = {
        #     'surname': "",
        #     'employee_number': '',
        #     'product': "sdgdsfgsdfgdsfgfdsg"
        # }


class ProductCreateForm(forms.ModelForm):
    '''Отображает форму добавления нового Изделия'''
    class Meta:
        model = Product
        fields = ('name',)


class ProductAddDetailForm(forms.ModelForm):
    '''Отображает форму добавления новой Детали в Изделие'''
    class Meta:
        model = Product
        fields = ('name',
                  'detail',)

        widgets = {
            'detail': autocomplete.ModelSelect2(url='data_autocomplete_detail'),
        }


class DetailCreateForm(forms.ModelForm):
    '''Отображает форму добавления новой Детали и Категории к которой она относится'''
    class Meta:
        model = Detail
        fields = ('name', 'category')

        widgets = {
            'category': autocomplete.ModelSelect2(url='data_autocomplete_category_detail'),
        }


class AddStageInDeatailForm(forms.ModelForm):
    '''Отображает форму добавления нового Этапа в Детали'''
    class Meta:
        model = StageManufacturingDetail
        fields = ('detail', 'order', 'name', 'operations', 'normalized_time', 'price')

# автозаполнение поля по переданному из CreateView pk
    def __init__(self, *args, **kwargs):
        id = kwargs.pop('pk')
        detail = Detail.objects.get(pk=id)
        super(AddStageInDeatailForm, self).__init__(*args, **kwargs)
        self.fields['detail'].initial = Detail.objects.get(pk=id)
        if StageManufacturingDetail.objects.filter(detail=detail):
            self.fields['order'].initial = \
                StageManufacturingDetail.objects.filter(detail=detail).order_by('-order')[0].order + 1


class EditStageInDetail(forms.ModelForm):
    '''Отображает форму редактирования Этапа в Детали'''
    class Meta:
        model = StageManufacturingDetail
        fields = ('__all__')



class WorkshopPlanCreateForm(forms.ModelForm):
    '''Отображает форму создания нового Плана'''
    class Meta:
        model = WorkshopPlan
        fields = ('__all__')


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
    '''Отображает форму редактирования Детали в Плане'''
    class Meta:
        model = WorkshopPlan
        fields = '__all__'


class CreateBatchDetailInPlanForm(forms.ModelForm):
    '''Отображает форму создания новой Партии Деталей'''
    comment = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = BatchDetailInPlan
        fields = ['workshopplan_detail', 'quantity_in_batch', 'sos', 'comment']

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('object')
        detail = name.split('_')[1]
        detail_id = Detail.objects.get(name=f'{detail}').id
        detail_in_plan = WorkshopPlan.objects.get(detail_id=detail_id)
        super(CreateBatchDetailInPlanForm, self).__init__(*args, **kwargs)
        self.fields['detail'].label = 'Деталь'
        self.fields['detail'].initial = detail_in_plan
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


class CreateNewStageManufacturingInWorkForm(forms.ModelForm):
    '''Форма задания(глагол) нового Этапа работы конкретной Партии Деталей'''
    comment_in_batch = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = StageManufacturingDetailInWork
        fields = ('batch', 'stage_in_batch', 'worker', 'in_work', 'time_of_work', 'comment_in_batch')

    def __init__(self, *args, **kwargs):
        batch_id = kwargs.pop('batch')
        stages = kwargs.pop('stages')
        super(CreateNewStageManufacturingInWorkForm, self).__init__(*args, **kwargs)
        self.fields['batch'].initial = batch_id
        self.fields['stage_in_batch'] = forms.ModelChoiceField(
                queryset=stages)

    def clean(self):
        batch = self.cleaned_data.get('batch')
        stage_in_batch = self.cleaned_data.get('stage_in_batch')
        comment = self.cleaned_data.pop('comment_in_batch')
        new_comment = Comment.objects.create(body=comment)
        self.cleaned_data.update({'comment_in_batch': new_comment})
        if StageManufacturingDetailInWork.objects.filter(batch_id=batch.id, stage_in_batch_id=stage_in_batch.id).exists():
            raise forms.ValidationError(f"Этап {stage_in_batch} в Партии {batch} уже есть!")



