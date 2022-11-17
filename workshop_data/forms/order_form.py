from dal import autocomplete
from django import forms

from sign.models import User
from workshop_data.models import StageManufacturingDetailInWork
from workshop_data.models.order import Order
from workshop_data.services import get_stage_in_work
from workshop_data.forms.stage_in_work_form import InitialsModelChoiceField


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


class TimeOfWorkInStageForm(forms.ModelForm):
    """Форма поля для ввода времени затраченного на работу в Наряде"""
    class Meta:
        model = StageManufacturingDetailInWork
        fields = ('time_of_work',)

    def clean(self):
        time_of_work = self.data['time'] # 'time' - <input  name="time" value="{{ form.time_of_work }}">
        stage = get_stage_in_work(self.instance.surname,
                              self.instance.batch.id,
                              self.instance.operations)
        stage.time_of_work = time_of_work
        stage.save()
