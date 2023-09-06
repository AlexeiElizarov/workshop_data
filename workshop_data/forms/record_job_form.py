from dal import autocomplete
from django import forms
from sign.models import User
from workshop_data.forms.stage_in_work_form import InitialsModelChoiceField
from workshop_data.models import Product, Detail, Month
from workshop_data.models.record_job import RecordJob
from workshop_data.models.detail import ParametersDetailForSPU


# class MyModelChoicesField(ModelChoiceField):
#     def label_from_instance(self, obj):
#         return f'{obj.name}'


class RecordJobForm(forms.ModelForm):
    """Отображает форму добавления новой записи о сделанных за день деталей"""
    user = forms.ModelChoiceField(
        label='Исполнитель',
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='data_autocomplete_worker_cpu')
    )

    product = forms.ModelChoiceField(
        label='Изделие',
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='data_autocomplete_product',
                                         forward=('detail',))

    )
    detail = forms.ModelChoiceField(
        queryset=Detail.objects.all(),
        label="Деталь",
        widget=autocomplete.ModelSelect2(url='data_autocomplete_detail_for_product',
                                         forward=('product',))
    )
    # month = forms.ModelChoiceField(
    #     label='Месяц',
    #     queryset=Month.objects.all(),
    #     widget=forms.TextInput(attrs={"class": "form-control", })
    # )
    quantity_1 = forms.IntegerField(
        label='Количество по 1й стороне',
        widget=forms.TextInput(attrs={"class": "form-control",})
    )
    quantity_2 = forms.IntegerField(
        label='Количество по 2й стороне',
        widget=forms.TextInput(attrs={"class": "form-control",})
    )
    quantity = forms.IntegerField(
        label='Количество по двум сторонам',
        widget=forms.TextInput(attrs={"class": "form-control", })
    )

    class Meta:
        model = RecordJob
        fields = '__all__'
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        super(RecordJobForm, self).__init__(*args, **kwargs)
        self.fields['quantity_1'].required = False
        self.fields['quantity_2'].required = False
        self.fields['quantity'].required = False


class ParametersDetailForSPUCreateForm(forms.ModelForm):
    """Форма ввода параметров детали на участке СПУ"""
    operations_first_side = forms.CharField(
        label='Операции 1й стороны',
        widget=forms.TextInput(attrs={"class": "form-control",})
    )
    operations_second_side = forms.CharField(
        label='Операции 2й стороны',
        widget=forms.TextInput(attrs={"class": "form-control", })
    )
    first_side_time = forms.FloatField(
        label='Время 1я сторона',
        widget=forms.TextInput(attrs={"class": "form-control", })
    )
    coefficient_first_side = forms.FloatField(
        label='Коэффициент 1',
        widget=forms.TextInput(attrs={"class": "form-control", })
    )
    second_side_time = forms.FloatField(
        label='Время 2я сторона',
        widget=forms.TextInput(attrs={"class": "form-control", })
    )
    coefficient_second_side = forms.FloatField(
        label='Коэффициент 2',
        widget=forms.TextInput(attrs={"class": "form-control", })
    )
    price = forms.FloatField(
        label='Расценка',
        widget=forms.TextInput(attrs={"class": "form-control", })
    )
    norm = forms.FloatField(
        label='Норма времени',
        widget=forms.TextInput(attrs={"class": "form-control", })
    )
    salary_per_first_side = forms.FloatField(
        label='Зарплата по 1-й стороне',
        widget=forms.TextInput(attrs={"class": "form-control",  'readonly': True})
    )
    salary_per_second_side = forms.FloatField(
        label='Зарплата по 2-й стороне',
        widget=forms.TextInput(attrs={"class": "form-control", 'readonly': True})
    )

    class Meta:
        model = ParametersDetailForSPU
        fields = '__all__'
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        super(ParametersDetailForSPUCreateForm, self).__init__(*args, **kwargs)
        self.fields['operations_first_side'].required = False
        self.fields['operations_second_side'].required = False
        self.fields['first_side_time'].required = False
        self.fields['second_side_time'].required = False
        self.fields['price'].required = False
        self.fields['coefficient_first_side'].required = False
        self.fields['coefficient_second_side'].required = False
        self.fields['salary_per_first_side'].required = False
        self.fields['salary_per_second_side'].required = False
        if kwargs.get('instance'):
            self.fields['salary_per_first_side'].initial = kwargs.get('instance').return_salary_per_first_side()
            self.fields['salary_per_second_side'].initial = kwargs.get('instance').return_salary_per_second_side()

    def clean(self):
        cleaned_data = super().clean()
        coefficient_first_side = cleaned_data.get('coefficient_first_side')
        coefficient_second_side = cleaned_data.get('coefficient_second_side')
        parameters = self.instance
        price = parameters.price
        t1 = parameters.first_side_time
        t2 = parameters.second_side_time
        d = parameters.return_salary_per_minute()
        if cleaned_data.get('coefficient_first_side') is not None:
            if cleaned_data.get('coefficient_first_side') != parameters.coefficient_first_side:
                parameters.coefficient_first_side = cleaned_data.get('coefficient_first_side')
                parameters.save()
                k1 = cleaned_data.get('coefficient_first_side')
                cleaned_data['coefficient_second_side'] = round((price - k1 * t1 * d) / (t2 * d), 3)
            elif cleaned_data.get('coefficient_second_side') != parameters.coefficient_second_side:
                parameters.coefficient_second_side = cleaned_data.get('coefficient_second_side')
                parameters.save()
                k2 = cleaned_data.get('coefficient_second_side')
                cleaned_data['coefficient_first_side'] = round((price - k2 * t2 * d) / (t1 * d), 3)
        return cleaned_data
