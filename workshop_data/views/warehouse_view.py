import datetime


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, CreateView, DeleteView, ListView, TemplateView, FormView

from sign.forms import User
from workshop_data.filters import WarehouseRecordsFilter
from workshop_data.models import Warehouse, Detail, Product
from workshop_data.forms.warehouse_form import WarehouseCreateForm, ViewWarehouseRecordForm
from workshop_data.models.detail import Prefix
from workshop_data.services import return_detail_by_product_detail_for_name


class WarehouseCreateView(LoginRequiredMixin, CreateView):
    """Отображает внесение количества деталей в кладовой"""
    model = Warehouse
    form_class = WarehouseCreateForm
    template_name = 'workshop_data/master/warehouse/create_new_record_warehouse.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        if form.is_valid():
            detail = form.cleaned_data['detail']
            semis = form.cleaned_data['semis']
            intermediate_detail = form.cleaned_data['intermediate_detail']
            income = form.cleaned_data['income']
            expenditures = form.cleaned_data['expenditures']
            try:
                warehouse_record = Warehouse(
                    date=datetime.datetime.now(),
                    section=form.cleaned_data['section'],
                    detail=detail,
                    product=form.cleaned_data['product'],
                    expenditures=expenditures,
                    income=income,
                    semis=semis,
                    balance_semis_on_this_moment=
                    detail.balance_semis_in_warehouse + income - expenditures if semis else
                    detail.balance_semis_in_warehouse,
                    intermediate_detail=intermediate_detail,
                    balance_intermediate_detail_on_this_moment=
                    detail.balance_intermediate_detail_in_warehouse + income - expenditures
                    if intermediate_detail else detail.balance_intermediate_detail_in_warehouse,
                    balance_in_warehouse_on_this_moment=
                    detail.get_balance_on_this_moment() + income - expenditures,
                    cell=form.cleaned_data['cell'],
                    employee=form.cleaned_data['employee'],
                    unit=form.cleaned_data['unit'],
                )
                warehouse_record.save()
            except IntegrityError:
                return HttpResponseRedirect(reverse_lazy('exeption_integrity_error'))
            if semis:
                detail.balance_semis_in_warehouse += income - expenditures
            elif intermediate_detail:
                detail.balance_intermediate_detail_in_warehouse += income - expenditures
            detail.save()
        if 'comment' in form.cleaned_data:
            form.cleaned_data['comment'].warehouse = warehouse_record
            form.cleaned_data['comment'].save()
        return HttpResponseRedirect(self.get_success_url())


class WarehouseCreateSelectedDetailView(WarehouseCreateView):
    template_name = 'workshop_data/master/warehouse/warehouse_list_detail_and_create_form.html'

    def get_form_kwargs(self):
        kwargs = super(WarehouseCreateSelectedDetailView, self).get_form_kwargs()
        kwargs.update(
            {'user': self.request.user._wrapped if hasattr(self.request.user, '_wrapped') else self.request.user})
        self.detail = return_detail_by_product_detail_for_name(self.kwargs['detail'], self.kwargs['product'])
        self.product = Product.objects.get(name=self.kwargs['product'])
        kwargs.update({'product': self.product, 'detail': self.detail})
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['records'] = ((Warehouse.objects.filter(detail=self.detail).
                               select_related('employee', 'product', 'detail__prefix')).
                              prefetch_related('warehousecomment_set')).order_by('-id')[:14][::-1]
        context['detail'] = self.detail
        context['product'] = self.product
        context['button_name'] = 'create'
        return context

    def get_success_url(self):
        return reverse_lazy("create_and_view_new_record_in_warehouse", kwargs={'product': self.product,
                                                                               'detail': self.detail})


class WarehouseDeleteView(LoginRequiredMixin, DeleteView):
    """Вьюха удаления Детали"""
    model = Warehouse
    template_name = 'workshop_data/master/warehouse/warehouse_delete_record.html'

    def get_object(self, **kwargs):
        return Warehouse.objects.get(id=self.kwargs.get('id'))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            detail = self.get_object().detail
            record = self.get_object()
            if record.semis:
                detail.balance_semis_in_warehouse -= record.income
                detail.balance_semis_in_warehouse += record.expenditures
            elif record.intermediate_detail:
                detail.balance_intermediate_detail_in_warehouse -= record.income
                detail.balance_intermediate_detail_in_warehouse += record.expenditures
            detail.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record'] = self.get_object()
        return context

    def get_form_kwargs(self):
        kwargs = super(WarehouseDeleteView, self).get_form_kwargs()
        # kwargs.update(
        #     {'user': self.request.user._wrapped if hasattr(self.request.user, '_wrapped') else self.request.user})
        self.detail = self.get_object().detail
        self.product = self.get_object().product
        return kwargs

    def get_success_url(self):
        return reverse_lazy("create_and_view_new_record_in_warehouse", kwargs={'product': self.get_object().product,
                                                                               'detail': self.get_object().detail})


class WarehouseUpdateView(LoginRequiredMixin, UpdateView):
    """Отображает изменения количества деталей в кладовой"""
    model = Warehouse
    form_class = WarehouseCreateForm
    template_name = 'workshop_data/master/warehouse/warehouse_list_detail_and_create_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        if form.is_valid():
            detail = form.cleaned_data['detail']
            semis = form.cleaned_data['semis']
            intermediate_detail = form.cleaned_data['intermediate_detail']
            income = form.cleaned_data['income']
            expenditures = form.cleaned_data['expenditures']
            if semis and form.initial['semis']: # если заготовка и была заготовка
                # баланс заготовок += приход - расход - приход(был) + расход(был)
                print()
                print('********1', 'з -> з')
                print()
                detail.balance_semis_in_warehouse += (
                        income - expenditures - form.initial['income'] + form.initial['expenditures'])
                self.object.balance_semis_on_this_moment = detail.balance_semis_in_warehouse
            elif intermediate_detail and form.initial['semis']: # если п/ф, а была заготовка
                print()
                print('********1', 'з -> п')
                print()
                # баланс заготовок -= приход(был)
                # баланс заготовок += расход(был)
                # баланс п/ф += приход - расход
                detail.balance_semis_in_warehouse -= form.initial['income']
                detail.balance_semis_in_warehouse += form.initial['expenditures']
                detail.balance_intermediate_detail_in_warehouse += income - expenditures
            elif intermediate_detail and form.initial['intermediate_detail']: # если п/ф и был п/ф
                print()
                print('********1', 'п-> п')
                print()
                detail.balance_intermediate_detail_in_warehouse += (
                        income - expenditures - form.initial['income'] + form.initial['expenditures'])
                self.object.balance_intermediate_detail_on_this_moment = detail.balance_intermediate_detail_in_warehouse
            elif semis and form.initial['intermediate_detail']: # если заготовка, а был п/ф
                print()
                print('********1', 'п -> з')
                print()
                # баланс п/ф -= приход(был)
                # баланс п/ф += расход(был)
                # баланс заготовок += приход - расход
                detail.balance_intermediate_detail_in_warehouse -= form.initial['income']
                detail.balance_intermediate_detail_in_warehouse += form.initial['expenditures']
                detail.balance_semis_in_warehouse += income - expenditures
            detail.save()
            self.object.balance_semis_on_this_moment = detail.balance_semis_in_warehouse
            self.object.balance_intermediate_detail_on_this_moment = detail.balance_intermediate_detail_in_warehouse
            self.object.balance_in_warehouse_on_this_moment = detail.get_balance_on_this_moment()
            self.object.save()
        if 'comment' in form.cleaned_data:
            form.cleaned_data['comment'].warehouse = self.object
            form.cleaned_data['comment'].save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(WarehouseUpdateView, self).get_form_kwargs()
        kwargs.update(
            {'user': self.request.user._wrapped if hasattr(self.request.user, '_wrapped') else self.request.user})
        self.detail = self.get_object().detail
        self.product = self.get_object().product
        kwargs.update({'product': self.product, 'detail': self.detail})
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['records'] = ((Warehouse.objects.filter(detail=self.detail).
                               select_related('employee', 'product', 'detail__prefix')).
                              prefetch_related('warehousecomment_set')).order_by('-id')[:14][::-1]
        context['detail'] = self.detail
        context['products'] = self.detail.detail_in_product
        context['button_name'] = 'update'
        return context

    def get_object(self, **kwargs):
        return Warehouse.objects.get(id=self.kwargs.get('id'))

    def get_success_url(self):
        return reverse_lazy("create_and_view_new_record_in_warehouse", kwargs={'product': self.get_object().product,
                                                                               'detail': self.get_object().detail})


class WarehouseListView(LoginRequiredMixin, ListView):
    """Отображает все записи по запросу"""
    model = Warehouse
    template_name = 'workshop_data/master/warehouse/warehouse_all_records_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        self.detail = return_detail_by_product_detail_for_name(self.kwargs['detail'], self.kwargs['product'])
        self.product = Product.objects.get(name=self.kwargs['product'])
        context['filter'] = WarehouseRecordsFilter(
            self.request.GET,
            queryset=Warehouse.objects.filter(detail=self.detail).
            select_related('employee', 'product', 'detail__prefix').
            prefetch_related('warehousecomment_set'))
        context['detail'] = self.detail
        context['product'] = self.product
        context['records'] = ((Warehouse.objects.filter(detail=self.detail).
                               select_related('employee', 'product', 'detail__prefix')).
                              prefetch_related('warehousecomment_set')).order_by('-id')[:14][::-1]
        context['all'] = 'all'
        return context


class ViewWarehouseRecord(FormView):
    """"""
    template_name = 'workshop_data/master/warehouse/enter_detail_in_form.html'
    form_class = ViewWarehouseRecordForm

    def form_valid(self, form):
        self.form = form
        return super(ViewWarehouseRecord, self).form_valid(form)

    def get_success_url(self):
        detail = self.form.cleaned_data['detail']
        product = self.form.cleaned_data['product']
        return reverse_lazy('create_and_view_new_record_in_warehouse', kwargs={'product': product,
                                                                               'detail': detail})
