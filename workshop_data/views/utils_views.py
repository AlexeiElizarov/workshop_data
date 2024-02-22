from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from workshop_data.forms.comment_form import CommentCreateForm

class CommentCreateViewMixin(LoginRequiredMixin, CreateView):
    model = None
    form_class = CommentCreateForm
    template_name = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user._wrapped if hasattr(self.request.user,'_wrapped') else self.request.user
        kwargs['object_id'] = self.kwargs.get('object')
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.workshop_plan = form.cleaned_data['object']
        super().form_valid(form)
        return super().form_valid(form)