from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User



class BaseRegisterForm(UserCreationForm):
    # email = forms.EmailField(label="Email")
    # first_name = forms.CharField(label="Имя")
    # last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "name",
                  "surname",
                  "patronymic",
                  "employee_number",
                  "employee_rank",
                  "position",
                  "birthday",
                  "gender",
                  "password1",
                  "password2", )
