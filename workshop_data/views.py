from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from dal import autocomplete
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import *
from .models import *
from sign.models import User
from django.utils.html import format_html
from django.db.models import Q



def sum_parametrs(list_objects):
    '''Считает сумму зарплаты списка нарядов '''
    lst = []
    for obj in list_objects:
        salary = float(obj.price) * int(obj.quantity) * 1.4
        lst.append(salary)
    return sum(lst)


class WorkerAutocomplete(autocomplete.Select2QuerySetView):
    '''Реализует поле автоподсказки Рабочего по вводимыи символам'''
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(surname__istartswith=self.q)
        return qs


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    '''Реализует поле автоподсказки Изделий по вводимыи символам'''
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()
        qs = Product.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class DetailAutocomplete(autocomplete.Select2QuerySetView):
    '''Реализует поле автоподсказки Деталей по вводимыи символам'''
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Detail.objects.none()
        qs = Detail.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


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
        user_id = User.objects.get(username=self.request.user).id
        context = super().get_context_data(**kwargs)
        if 'month' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id).filter(month=self.kwargs['month'])
            context['salary'] = sum_parametrs(context['orders'])
            context['month'] = context['orders'][0]
        elif 'product' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id).\
                filter(product_id=Product.objects.get(name=self.kwargs['product']))
        elif 'detail' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id).\
                filter(detail_id=Detail.objects.get(name=self.kwargs['detail']))
        elif 'category' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id).\
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


class ProductCreateView(CreateView):
    '''Отображает страницу создания нового Изделия'''
    model = Product
    form_class = ProductCreateForm
    template_name = 'workshop_data/worker/product_create.html'
    success_url = reverse_lazy('create_new_product_complite')


class DetailCreateView(CreateView):
    '''Отображает страницу создания новоой Детали'''
    model = Detail
    form_class = DetailCreateForm
    template_name = 'workshop_data/worker/detail_create.html'
    success_url = reverse_lazy('create_new_detail_complite')


def product_create_complite(request):
    return render(request, 'workshop_data/worker/product_create_complite.html')

def detaile_create_complite(request):
    return render(request, 'workshop_data/worker/detail_create_complite.html')


####################################         MASTER          ###########################################


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
        print(self.kwargs)
        return context


class WorkerOrdersListForMaster(ListView):
    model = Order
    login_url = '/login/'
    template_name = 'workshop_data/worker/orders_user_parametr_list.html' # шаблон из OrderUserParametrListView
    context_object_name = 'orders'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        if 'surname' in self.kwargs and 'month' not in self.kwargs:
            print('****surname')
            context['orders'] = Order.objects.filter(
                surname_id=User.objects.filter(
                    surname=self.kwargs['surname'], name=self.kwargs['name'])[0].id)
        elif 'month' in self.kwargs:
            print('****month')
            context['orders'] = Order.objects.filter(
                surname_id=User.objects.filter(
                    surname=self.kwargs['surname'], name=self.kwargs['name'])[0].id).filter(
                month=self.kwargs['month']
            )
            context['month'] = context['orders'][0]
        return context
