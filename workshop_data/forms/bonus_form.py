from dal import autocomplete
from django import forms

from workshop_data.forms.stage_in_work_form import InitialsModelChoiceField
from workshop_data.models import Bonus
from sign.models import User
from workshop_data.models.comment import Comment


class CreateNewBonusForm(forms.ModelForm):
    """Отображает форму создание новой Премии(Bonus) работнику"""
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Bonus
        fields = ('worker', 'month', 'quantity', 'time', 'comment',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(CreateNewBonusForm, self).__init__(*args, **kwargs)
        self.fields['worker'] = InitialsModelChoiceField(
            queryset=User.objects.all(),
            label='Рабочий',
            widget=autocomplete.ModelSelect2(url='data_autocomplete_worker')
        )

    def clean(self):
        comment = self.cleaned_data.pop('comment')
        new_comment = Comment.objects.create(body=comment, author=self.user)
        self.cleaned_data.update({'comment': new_comment})
