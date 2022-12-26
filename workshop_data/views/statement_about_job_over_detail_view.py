from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from workshop_data.forms import StatementAboutJobOverDetailForm
from workshop_data.models import (
    StatementAboutJobOverDetail,
    ResolutionForStatementAboutJobOverDetail)


class StatementAboutJobOverDetailView(LoginRequiredMixin, CreateView):
    """Заявление на работу над Деталью"""
    model = StatementAboutJobOverDetail
    form_class = StatementAboutJobOverDetailForm
    template_name = 'workshop_data/master/statement_for_detail/statement_about_job_over_detail.html'

    def form_valid(self, form):
        statement = form.save(commit=False)
        if form.is_valid():
            statement.worker = self.request.user
            statement.save()
            resolution = ResolutionForStatementAboutJobOverDetail(
                statement=statement,
                master=None,
                resolution=False,
            )
            resolution.save()
        return HttpResponseRedirect(reverse_lazy('list_all_resolution_or_not_detail', kwargs={'username': self.request.user}))


class AllDetailResolutionOrNotView(LoginRequiredMixin, ListView):
    """Список всех Деталей заявленных для работы(одобренные или нет)"""
    model = StatementAboutJobOverDetail
    template_name = 'workshop_data/master/statement_for_detail/list_all_detail_resolution_or_not.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.position == "MSR":
            context['statements'] = StatementAboutJobOverDetail.objects.all().order_by('date_statement')
        else:
            context['statements'] = StatementAboutJobOverDetail.objects.filter(worker=self.request.user).order_by('date_statement')
        return context


