from django import forms

from workshop_data.models import Warehouse, Comment


class WarehouseCreateForm(forms.ModelForm):
    """"""
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"}),
        label="Комментарий")
    class Meta:
        model = Warehouse
        fields = ['section', 'semis', 'intermediate_detail', 'unit', 'comment']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(WarehouseCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        comment = self.cleaned_data.pop('comment')
        new_comment = Comment.objects.create(body=comment, author=self.user)
        self.cleaned_data.update({'comment': new_comment})