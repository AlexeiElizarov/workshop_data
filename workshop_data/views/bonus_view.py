from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from workshop_data.forms.bonus_form import CreateNewBonusForm
from workshop_data.models.bonus import Bonus
from workshop_data.filters import BonusFilter
from sign.models import User
from workshop_data.services import get_average_cost_per_hour, get_list_all_workers


class CreateNewBonusView(LoginRequiredMixin, CreateView):
    """Модель описывает страницу добавления новой Премии(Bonus) работнику"""
    model = Bonus
    form_class = CreateNewBonusForm
    template_name = 'workshop_data/master/bonus/create_new_bonus.html'
    success_url = reverse_lazy('start_new_stage_in_work_complete')  # FIXME

    def get_form_kwargs(self):
        kwargs = super(CreateNewBonusView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        if object.time:
            object.quantity = object.time * get_average_cost_per_hour(object.worker.id)
        elif object.quantity:
            object.time = 0
        object.save()
        return render(self.request,
                      'workshop_data/master/bonus/create_new_bonus_complete.html',
                      {
                          'bonus': object.quantity,
                          'worker': object.worker
                      })


class ListAllBonuses(LoginRequiredMixin, ListView):
    """Страница всех премий"""
    model = Bonus
    template_name = 'workshop_data/master/bonus/list_bonuses_all_wokrers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['bonuses'] = Bonus.objects.all().order_by('date')
        context['filter'] = BonusFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ListAllWorkersAndBonuses(LoginRequiredMixin, ListView):
    """Страница всех Работников и их Премий"""
    model = User
    template_name = 'workshop_data/master/bonus/list_worker_and_here_bonus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if 'month' in self.request.GET:
            context['month'] = self.request.GET['month']
        context['workers'] = get_list_all_workers().order_by('position')
        context['filter'] = BonusFilter(self.request.GET, queryset=self.get_queryset())
        return context


class UpdateBonusView(LoginRequiredMixin, UpdateView):
    """Редактирование записи о Премии(Bonus)"""
    template_name = 'workshop_data/master/bonus/create_new_bonus.html'
    form_class = CreateNewBonusForm
    success_url = reverse_lazy('list_bonuses_all_worker')

    def get_object(self, **kwargs):
        return Bonus.objects.get(id=self.kwargs.get('id'))

    def get_form_kwargs(self):
        kwargs = super(UpdateBonusView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
