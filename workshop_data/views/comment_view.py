from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from workshop_data.models import Comment
from workshop_data.forms.comment_form import CommentEditForm


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование комментария"""
    model = Comment
    form_class = CommentEditForm
    template_name = ''
    success_url = 'plan'

    def get_object(self, **kwargs):
        object = self.kwargs.get('object')
        return object