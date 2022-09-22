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
            'operations': forms.CheckboxSelectMultiple(
                choices=NUMBERS_OPERATIONS,)
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


class CreateBatchDetailInPlanForm(forms.ModelForm):
    '''Отображает форму создания новой Партии Деталей'''
    comment = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = BatchDetailInPlan
        # fields = ('__all__')
        fields = ['detail', 'quantity_in_batch', 'sos', 'comment']
        # widgets = {
        #     'comment': forms.Textarea
        # }

    def __init__(self, *args, **kwargs):
        # self.detail = kwargs.pop('detail')
        # self.product = kwargs.pop('product')
        name = kwargs.pop('object')
        product = name.split('_')[0]
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
