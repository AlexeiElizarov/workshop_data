from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

from workshop_data.forms.order_form import TimeOfWorkInStageForm
from workshop_data.models.order import Order
from workshop_data.models.product import Product
from workshop_data.models.detail import Detail
from workshop_data.forms import OrderForm
from sign.models import User
from workshop_data.models.stage_manufacturing_detail_in_work import  StageManufacturingDetailInWork
from workshop_data.services.services import get_stage_in_work



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
                author_id=self.request.user.id,
            )
            order.save()
        return redirect('orders_user_list_all', username=current_user.username)


class OrderUserParametrListView(LoginRequiredMixin, ListView):
    '''Отображает наряды пользователя фильтруя их в зависимости от переданного параметра'''
    model = Order
    login_url = '/login/'
    context_object_name = 'orders'
    template_name = 'workshop_data/worker/order/orders_user_parametr_list.html'

    def get_context_data(self, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        context = super().get_context_data(**kwargs)
        # stage_work = get_stage_in_work(self.request, user, )
        if 'month' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user.id).filter(month=self.kwargs['month'])
            context['month'] = context['orders'][0]
        elif 'product' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user.id). \
                filter(product_id=Product.objects.get(name=self.kwargs['product']))
        elif 'detail' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user.id). \
                filter(detail_id=Detail.objects.get(name=self.kwargs['detail']))
        elif 'category' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user.id). \
                filter(detail__category__name=self.kwargs['category'])
        else:
            context['orders'] = Order.objects.filter(surname_id=user.id)
        # context['stage_work'] = get_stage_in_work(self.)
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


class TimeOfWorkInStage(UpdateView):
    """"""
    template_name = 'workshop_data/worker/order/time_of_work_form.html'
    form_class = TimeOfWorkInStageForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return Order.objects.get(pk=id)

    def get_success_url(self):
        return reverse('orders_user_list_all', kwargs={'username': self.request.user})
