from django import forms

from workshop_data.models.comment import Comment


class CommentEditForm(forms.ModelForm):
    """Отображает форму редактирования детали"""

    class Meta:
        model = Comment
        fields = ('body',)