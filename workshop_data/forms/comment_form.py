from django import forms

from workshop_data.models import WorkshopPlan
from workshop_data.models.comment import (
    Comment,
    WorkshopPlanComment,)



class CommentEditForm(forms.ModelForm):
    """Отображает форму редактирования детали"""

    class Meta:
        model = Comment
        fields = ('body',)


class CommentCreateForm(forms.ModelForm):
    """
    Форма добавления нового комментария в План
    """

    class Meta:
        model = WorkshopPlanComment
        fields = ('body', 'author')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.workshop_plan_object_id = kwargs.pop('object_id')
        super(CommentCreateForm, self).__init__(*args, **kwargs)
        self.fields['body'].required = False
        self.fields['author'].required = False

    def clean(self):
        wp = WorkshopPlan.objects.get(id=int(self.workshop_plan_object_id))
        self.cleaned_data.update({'object': wp})
        return self.cleaned_data