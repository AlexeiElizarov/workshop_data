import datetime
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

from workshop_data.forms.order_form import TimeOfWorkInStageForm
from workshop_data.models.order import Order
from workshop_data.models.product import Product
from workshop_data.models.detail import Detail
from workshop_data.forms import OrderForm
from sign.models import User, LIST_POSITION_WORKER
from workshop_data.models.stage_manufacturing_detail_in_work import  StageManufacturingDetailInWork
from workshop_data.services import get_average_price_orders, get_average_price_orders_per_month, \
    get_average_cost_per_hour, get_average_cost_per_hour_per_month
from workshop_data.services.general_services import get_stage_in_work



class OrderUserCreateView(LoginRequiredMixin, CreateView):
    '''Отображает страницу заполнения нового наряда'''
    model = Order
    form_class = OrderForm
    template_name = 'workshop_data/worker/order_user_create_view.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.is_valid():
            order_object = Order(
                date=datetime.datetime.now(),
                month=form.cleaned_data['month'],
                # workshop=form.cleaned_data['workshop'],
                # section=form.cleaned_data['section'],
                user=self.object.user,
                employee_number=self.object.user.employee_number,
                product=form.cleaned_data['product'],
                detail=form.cleaned_data['detail'],
                operations=form.cleaned_data['operations'],
                quantity=form.cleaned_data['quantity'],
                normalized_time=form.cleaned_data['normalized_time'],
                price=form.cleaned_data['price'],
                author_id=self.request.user.id,
            )
        #     order.save()
        # return redirect('orders_user_list_all', username=current_user.username)
        args = {}
        args['order'] = order_object
        if 'view' in self.request.POST:
            return render(self.request, 'workshop_data/order_template_for_print.html', args)
        elif 'save' in self.request.POST:
            order_object.author =self.request.user
            order_object.save()
            # self.object.author = self.request.user
            # self.object.save()
            return HttpResponseRedirect(reverse_lazy('start_new_stage_in_work_complete'))


class OrderUserParametrListView(LoginRequiredMixin, ListView):
    '''Отображает наряды пользователя фильтруя их в зависимости от переданного параметра'''
    model = Order
    login_url = '/login/'
    context_object_name = 'orders'
    template_name = 'workshop_data/worker/order/orders_user_parametr_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.position == 'MSR':
            user = User.objects.get(
                surname=self.kwargs['surname'], name=self.kwargs['name'])
        elif self.request.user.position in LIST_POSITION_WORKER:
            user = User.objects.get(username=self.request.user.username)
        if 'month' in self.kwargs:
            month = self.kwargs['month']
            context['orders'] = Order.objects.filter(user_id=user.id).filter(month=month).order_by('date')
            context['month'] = month
            context['average_cost_per_hour_per_month'] = get_average_cost_per_hour_per_month(user.id, month)
            context['average_price_per_month'] = get_average_price_orders_per_month(user, month)
        elif 'product' in self.kwargs:
            context['orders'] = Order.objects.filter(user_id=user.id). \
                filter(product_id=Product.objects.get(name=self.kwargs['product'])).order_by('date')
        elif 'detail' in self.kwargs:
            context['orders'] = Order.objects.filter(user_id=user.id). \
                filter(detail_id=Detail.objects.get(name=self.kwargs['detail'])).order_by('date')
        elif 'category' in self.kwargs:
            context['orders'] = Order.objects.filter(user_id=user.id). \
                filter(detail__category__name=self.kwargs['category']).order_by('date')
        else:
            context['orders'] = Order.objects.filter(user_id=user.id).order_by('date')
        context['average_price'] = get_average_price_orders(user)
        context['average_cost_per_hour'] = get_average_cost_per_hour(user.id)
        return context


class OrderUserEditView(LoginRequiredMixin, UpdateView):
    '''Редактирование наряда'''
    template_name = 'workshop_data/worker/order_user_create_view.html'
    form_class = OrderForm

    # success_url = reverse_lazy('orders_user_list_all') # FIXME    + git

    def get_success_url(self, **kwargs):
        return reverse("orders_user_list_all", kwargs={'username': self.kwargs['username']})

    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return Order.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    '''Удаление наряда'''
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
