from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class BaseRegisterForm(UserCreationForm):
    # email = forms.EmailField(label="Email")
    # first_name = forms.CharField(label="Имя")
    # last_name = forms.CharField(label="Фамилия")

    class Meta(UserCreationForm.Meta):
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
