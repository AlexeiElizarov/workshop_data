from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView
from sign.models import User, LIST_POSITION_WORKER
from workshop_data.models.order import Order
from workshop_data.services import get_average_price_orders, get_average_price_orders_per_month


class WorkerListView(LoginRequiredMixin, ListView):
    """Отображает страницу всех работников(или выборка по специальности)"""
    model = User
    login_url = '/login/'
    template_name = 'workshop_data/master/workers/workers_parametr_list.html'
    context_object_name = 'workers'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if not 'position' in self.kwargs:
            context['workers'] = User.objects.filter(~Q(position='MSR') & ~Q(position='EPB'))
        elif self.kwargs['position'] == 'LSM':
            context['workers'] = User.objects.filter(position='LSM')
        elif self.kwargs['position'] == 'TRN':
            context['workers'] = User.objects.filter(position='TRN')
        elif self.kwargs['position'] == 'MLR':
            context['workers'] = User.objects.filter(position='MLR')
        return context


# class WorkerOrdersListForMaster(LoginRequiredMixin, ListView):
#     """Показывает наряды работников(все, по месяцам)"""
#     model = Order
#     login_url = '/login/'
#     template_name = 'workshop_data/worker/order/orders_user_parametr_list.html'  # шаблон из OrderUserParametrListView
#     context_object_name = 'orders'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = User.objects.filter(
#                     surname=self.kwargs['surname'], name=self.kwargs['name'])[0]
#         if 'surname' in self.kwargs and 'month' not in self.kwargs:
#             context['orders'] = Order.objects.filter(
#                 user_id=user.id)
#         elif 'month' in self.kwargs:
#             month = self.kwargs['month']
#             context['orders'] = Order.objects.filter(
#                 user_id=user.id).filter(month=self.kwargs['month'])
#             context['month'] = month
#             context['average_price_for_month'] = get_average_price_orders_per_month(user, month)
#         context['average_price'] = get_average_price_orders(user)
#         return context


class WorkerAveragePriceListForMaster(LoginRequiredMixin, ListView):
    """Отображает страницу работников и их средней расценки по нарядам"""
    model = Order
    login_url = '/login/'
    template_name = 'workshop_data/master/workers/workers_average_price_order.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workers'] = User.objects.filter(position__in=LIST_POSITION_WORKER)
        return context