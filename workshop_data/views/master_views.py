from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView
from sign.models import User
from ..models import Order


class WorkerListView(LoginRequiredMixin, ListView):
    '''Отображает страницу всех работников(или выборка по специальности)'''
    model = User
    login_url = '/login/'
    template_name = 'workshop_data/master/workers_parametr_list.html'
    context_object_name = 'workers'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'LSM' in self.kwargs:
            context['workers'] = User.objects.filter(position='LSM')
        elif 'TRN' in self.kwargs:
            context['workers'] = User.objects.filter(position='TRN')
        else:
            context['workers'] = User.objects.filter(~Q(position='MSR'))
        return context


class WorkerOrdersListForMaster(ListView):
    '''Показывает все наряды всех работников'''
    model = Order
    login_url = '/login/'
    template_name = 'workshop_data/worker/orders_user_parametr_list.html'  # шаблон из OrderUserParametrListView
    context_object_name = 'orders'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'surname' in self.kwargs and 'month' not in self.kwargs:
            context['orders'] = Order.objects.filter(
                surname_id=User.objects.filter(
                    surname=self.kwargs['surname'], name=self.kwargs['name'])[0].id)
        elif 'month' in self.kwargs:
            context['orders'] = Order.objects.filter(
                surname_id=User.objects.filter(
                    surname=self.kwargs['surname'], name=self.kwargs['name'])[0].id).filter(
                month=self.kwargs['month']
            )
            context['month'] = context['orders'][0]
        return context
