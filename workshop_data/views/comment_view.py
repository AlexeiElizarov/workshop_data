from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from workshop_data.models import Comment
from workshop_data.forms.comment_form import CommentEditForm, CommentCreateForm
from workshop_data.models.comment import WorkshopPlanComment
from workshop_data.services import current_year
from workshop_data.views.utils_views import CommentCreateViewMixin


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование комментария"""
    model = Comment
    form_class = CommentEditForm
    template_name = ''
    success_url = 'plan'

    def get_object(self, **kwargs):
        object = self.kwargs.get('object')
        return object


class WorkshopPlanCommentCreateView(CommentCreateViewMixin):
    model = WorkshopPlanComment
    template_name = 'comments/workshop_plan_comments_create.html'

    # success_url = reverse_lazy('plan')

    def get_success_url(self):
        return reverse('plan_year_month', kwargs=({'year': current_year(),
                                        'month': self.kwargs.get('month'),
                                        }))
