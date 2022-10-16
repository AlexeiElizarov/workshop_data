from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from ..models import Order
from ..forms import OrderForm
from .services_view import *



class OrderUserCreateView(LoginRequiredMixin, CreateView):
    '''Отображает страницу заполнения нового наряда'''
    model = Order
    form_class = OrderForm
    template_name = 'workshop_data/worker/order_user_create_view.html'

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> "HttpResponse":
        form = self.form_class(request.POST)
        current_user = request.user
        if form.is_valid():
            order = Order(
                # date=request.POST['date'],
                month=form.cleaned_data['month'],
                # workshop=form.cleaned_data['workshop'],
                # section=form.cleaned_data['section'],
                surname_id=User.objects.get(username=current_user.username).id,
                employee_number=current_user.employee_number,
                product=form.cleaned_data['product'],
                detail=form.cleaned_data['detail'],
                operations=form.cleaned_data['operations'],
                quantity=form.cleaned_data['quantity'],
                normalized_time=form.cleaned_data['normalized_time'],
                price=form.cleaned_data['price'],
            )
            order.save()
        return redirect('orders_user_list_all', username=current_user.username)


class OrderUserParametrListView(LoginRequiredMixin, ListView):
    '''Отображает наряды пользователя фильтруя их в зависимости от переданного параметра'''
    model = Order
    login_url = '/login/'
    context_object_name = 'orders'
    template_name = 'workshop_data/worker/orders_user_parametr_list.html'

    def get_context_data(self, *args, **kwargs):
        user_id = User.objects.get(username=self.request.user.username).id
        context = super().get_context_data(**kwargs)
        if 'month' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id).filter(month=self.kwargs['month'])
            context['salary'] = sum_parametrs(context['orders'])
            context['month'] = context['orders'][0]
        elif 'product' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id). \
                filter(product_id=Product.objects.get(name=self.kwargs['product']))
        elif 'detail' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id). \
                filter(detail_id=Detail.objects.get(name=self.kwargs['detail']))
        elif 'category' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id). \
                filter(detail__category__name=self.kwargs['category'])
        else:
            context['orders'] = Order.objects.filter(surname_id=user_id)
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


class OrderDeleteView(DeleteView):
    '''Удаление наряда'''
    template_name = 'workshop_data/worker/order_user_delete_view.html'
    queryset = Order.objects.all()

    def get_success_url(self, **kwargs):
        return reverse("orders_user_list_all", kwargs={'username': self.kwargs['username']})

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return Order.objects.get(pk=id)