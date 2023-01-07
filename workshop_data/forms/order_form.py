from dal import autocomplete
from django import forms

from sign.models import User, LIST_POSITION_WORKER
from workshop_data.models import StageManufacturingDetailInWork
from workshop_data.models.order import Order
from workshop_data.services import get_stage_in_work
from workshop_data.forms.stage_in_work_form import InitialsModelChoiceField


class OrderForm(forms.ModelForm):
    """Отображает форму добавления нового Наряда"""
    class Meta:
        model = Order
        fields = ('month',
                  'user',
                  'product',
                  'detail',
                  # 'batch',
                  'operations',
                  'quantity',
                  'normalized_time',
                  'price',)
        widgets = {
            'product': autocomplete.ModelSelect2(url='data_autocomplete_product'),
            'detail': autocomplete.ModelSelect2(url='data_autocomplete_detail'),
            # 'batch': autocomplete.ModelSelect2(url='data_autocomplete_batch'),
        }
        # help_texts = {
        #     'surname': "",
        #     'employee_number': '',
        #     'product': "sdgdsfgsdfgdsfgfdsg"
        # }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['user'] = InitialsModelChoiceField(
            queryset=User.objects.all(),
            label='Рабочий',
            widget=autocomplete.ModelSelect2(url='data_autocomplete_worker')
        )


class TimeOfWorkInStageForm(forms.ModelForm):
    """Форма поля для ввода времени затраченного на работу в Наряде"""

    class Meta:
        model = Order
        fields = ('time_of_work_order',)

    def clean(self):
        time_of_work = self.data['time']  # 'time' - <input  name="time" value="{{ form.time_of_work }}">
        # stage = get_stage_in_work(self.instance.user,
        #                           self.instance.batch.id,
        #                           self.instance.operations)
        # stage.time_of_work_stage = time_of_work
        # stage.save()
        self.instance.time_of_work_order = time_of_work
        self.instance.save()
