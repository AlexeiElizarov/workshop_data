import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView, RedirectView, TemplateView

from workshop_data.filters import OrdersFilter
from workshop_data.forms.order_form import TimeOfWorkInStageForm, OrderEditMonthForm
from workshop_data.models.order import Order
from workshop_data.models.product import Product
from workshop_data.models.detail import Detail
from workshop_data.forms import OrderForm
from sign.models import User, LIST_POSITION_WORKER
from workshop_data.services import (
    get_average_price_orders, get_average_price_orders_per_month,
    get_average_cost_per_hour, get_average_cost_per_hour_per_month,
    get_order_by_user)


class OrderUserCreateView(LoginRequiredMixin, CreateView):
    """Отображает страницу заполнения нового наряда"""
    model = Order
    form_class = OrderForm
    template_name = 'workshop_data/worker/order_user_create_view.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.is_valid():
            order_object = Order(
                date=datetime.datetime.now(),
                month=form.cleaned_data['month'],
                # # workshop=form.cleaned_data['workshop'],
                # # section=form.cleaned_data['section'],
                user=self.object.user,
                employee_number=self.object.user.employee_number,
                product=self.object.product,
                detail=self.object.detail,
                batch=None,
                operations=form.cleaned_data['operations'],
                stage=self.object.stage,
                quantity=form.cleaned_data['quantity'],
                normalized_time=form.cleaned_data['normalized_time'],
                price=form.cleaned_data['price'],
                author_id=self.request.user.id,
            )
            args = {'order': order_object}
            if 'view' in self.request.POST:
                if self.object.quantity:
                    return render(self.request, 'workshop_data/order_template_for_print_2_list.html', args)
                else:
                    #return render(self.request, 'workshop_data/order_template_for_print.html', args)
                    return render(self.request, 'workshop_data/order_.html', args)
            elif 'state' in self.request.POST:
                return render(self.request, 'workshop_data/order_state.html', args)
            elif 'save' in self.request.POST:
                order_object.author = self.request.user
                order_object.save()
                # self.object.author = self.request.user
                # self.object.save()
                return HttpResponseRedirect(reverse_lazy('start_new_stage_in_work_complete'))


class AllOrderForAllWorker(LoginRequiredMixin, ListView):
    """Отображает все наряды всех работников"""
    model = Order
    context_object_name = 'orders'
    template_name = 'workshop_data/master/orders/orders_all_list_for_master.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_date'] = OrdersFilter(self.request.GET)
        orders = Order.objects.all().order_by('-date').\
            select_related('batch', 'detail__category', 'product', 'user', 'stage')
        context['average_price'] = get_average_price_orders(orders)
        context['average_cost_per_hour'] = get_average_cost_per_hour(orders)
        if 'month' in self.kwargs:
            month = self.kwargs['month']
            orders = orders.filter(month=month).order_by('date'). \
                select_related('batch', 'detail__category', 'product', 'user',)
            context['orders'] = orders
            context['month'] = month
            context['average_cost_per_hour_per_month'] = get_average_cost_per_hour_per_month(orders)
            context['average_price_per_month'] = get_average_price_orders_per_month(orders)
        elif 'username' in self.kwargs:
            context['orders'] = orders.filter(user=User.objects.get(username=self.kwargs.get('username')))
        elif 'product' in self.kwargs:
            context['orders'] = orders.filter(product_id=Product.objects.get(name=self.kwargs['product']))
        elif 'detail' in self.kwargs:
            context['orders'] = orders.filter(detail_id=Detail.objects.get(name=self.kwargs['detail']))
        elif 'category' in self.kwargs:
            context['orders'] = orders.filter(detail__category__name=self.kwargs['category'])
        else:
            context['orders'] = orders
        return context


class OrderUserParametrListView(LoginRequiredMixin, ListView):
    """Отображает наряды пользователя фильтруя их в зависимости от переданного параметра"""
    model = Order
    context_object_name = 'orders'
    template_name = 'workshop_data/worker/order/orders_user_parametr_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.position == 'MSR':
            user = User.objects.get(
                username=self.kwargs['username'])
        elif self.request.user.position in LIST_POSITION_WORKER:
            user = User.objects.get(username=self.request.user.username)

        orders = Order.objects.all().order_by('date').filter(user_id=user.id).\
                select_related('batch', 'detail__category', 'product', 'user', 'stage')
        context['average_price'] = get_average_price_orders(orders)
        context['average_cost_per_hour'] = get_average_cost_per_hour(orders)

        if 'month' in self.kwargs:
            month = self.kwargs['month']
            orders = orders.filter(user_id=user.id).filter(month=month).order_by('date'). \
                select_related('batch', 'detail__category', 'product', 'user')
            context['orders'] = orders
            context['month'] = month
            context['average_cost_per_hour_per_month'] = get_average_cost_per_hour_per_month(orders)
            context['average_price_per_month'] = get_average_price_orders_per_month(orders)
        elif 'product' in self.kwargs:
            context['orders'] = orders.filter(product_id=Product.objects.get(name=self.kwargs['product']))
        elif 'detail' in self.kwargs:
            context['orders'] = orders.filter(detail_id=Detail.objects.get(name=self.kwargs['detail']))
        elif 'category' in self.kwargs:
            context['orders'] = orders.filter(detail__category__name=self.kwargs['category'])
        else:
            context['orders'] = orders
        return context


class OrderUserEditView(LoginRequiredMixin, UpdateView):
    """Редактирование наряда"""
    model = Order
    template_name = 'workshop_data/worker/order_user_create_view.html'
    form_class = OrderForm

    # success_url = reverse_lazy('orders_user_list_all') # FIXME    + git

    def get_success_url(self, **kwargs):
        return reverse("orders_user_list_all", kwargs={'username': self.kwargs['username']})

    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return Order.objects.get(pk=id)


class OrderUserEditMonthView(LoginRequiredMixin, UpdateView):
    """Редактирование работником месяца в наряде """
    model = Order
    template_name = 'workshop_data/worker/order/order_user_edit_month.html'
    form_class = OrderEditMonthForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return Order.objects.get(pk=id)

    def get_success_url(self, **kwargs):
        return reverse("orders_user_list_all", kwargs={'username': self.kwargs['username']})


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление наряда"""
    template_name = 'workshop_data/worker/order_user_delete_view.html'
    queryset = Order.objects.all()

    def get_success_url(self, **kwargs):
        return reverse("orders_user_list_all", kwargs={'username': self.kwargs['username']})

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return Order.objects.get(pk=id)


class TimeOfWorkInStage(LoginRequiredMixin, UpdateView):
    """"""
    template_name = 'workshop_data/worker/order/time_of_work_form.html'
    form_class = TimeOfWorkInStageForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return Order.objects.get(pk=id)

    def get_success_url(self):
        return reverse('orders_user_list_all', kwargs={'username': self.request.user})


# class ViewingTemplateOrderView(LoginRequiredMixin, TemplateView):
#     """Предварительный просмотр наряда для печати"""
#
#     template_name = 'workshop_data/order_template_for_print.html'
