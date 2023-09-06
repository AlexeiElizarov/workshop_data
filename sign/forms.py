import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import SelectDateWidget

User = get_user_model()


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class BaseRegisterForm(UserCreationForm):
    # email = forms.EmailField(label="Email")
    # first_name = forms.CharField(label="Имя")
    # last_name = forms.CharField(label="Фамилия")
    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year - 70, cur_year)])
    birthday = forms.DateField(initial=datetime.date.today(),
                               label="День Рождения",
                               widget=SelectDateWidget(years=year_range))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",
                  "name",
                  "surname",
                  "patronymic",
                  "employee_number",
                  "position",
                  "employee_rank",
                  "birthday",
                  "gender",
                  "password1",
                  "password2", )
