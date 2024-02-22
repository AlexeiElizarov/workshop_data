from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, CreateView, DeleteView, ListView, TemplateView, FormView

from workshop_data.filters import WarehouseRecordsFilter
from workshop_data.models import Warehouse, Detail
from workshop_data.forms.warehouse_form import WarehouseCreateForm, ViewWarehouseRecordForm
from workshop_data.models.detail import Prefix
from workshop_data.services import return_detail_by_product_detail_for_name


class WarehouseCreateView(LoginRequiredMixin, CreateView):
    """Отображает внесение количества деталей в кладовой"""
    model = Warehouse
    form_class = WarehouseCreateForm
    template_name = 'workshop_data/plan/warehouse/create_new_record_warehouse.html'
    success_url = reverse_lazy('plan')


    def get_form_kwargs(self):
        kwargs = super(WarehouseCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user._wrapped if hasattr(self.request.user,'_wrapped') else self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        if self.object.semis:
            self.object.detail.balance_semis_in_warehouse += self.object.income
            self.object.detail.balance_semis_in_warehouse -= self.object.expenditures
        elif self.object.intermediate_detail:
            print()
            print('********', )
            print('1', self.object.detail.balance_intermediate_detail_in_warehouse)
            print('2', self.object.income)
            print('3', self.object.expenditures)
            print()
            self.object.detail.balance_intermediate_detail_in_warehouse += self.object.income
            self.object.detail.balance_intermediate_detail_in_warehouse -= self.object.expenditures
        self.object.detail.save()
        return super().form_valid(form)


class WarehouseUpdateView(LoginRequiredMixin, UpdateView):
    """Отображает изменения количества деталей в кладовой"""
    model = Warehouse
    form_class = WarehouseCreateForm
    template_name = 'workshop_data/plan/warehouse/create_new_record_warehouse.html'
    success_url = reverse_lazy('plan')

    def get_form_kwargs(self):
        kwargs = super(WarehouseUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class WarehouseListView(LoginRequiredMixin, ListView):
    """Отображает все записи по запросу"""
    model = Warehouse
    template_name = 'workshop_data/plan/warehouse/warehouse_list_all.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = WarehouseRecordsFilter(
            self.request.GET,
            queryset=self.get_queryset().order_by('-date'))
        detail = return_detail_by_product_detail_for_name(self.kwargs['detail'], self.kwargs['product'])
        context['records'] = Warehouse.objects.filter(detail=detail)
        return context


class ViewWarehouseRecord(FormView):
    """"""
    template_name = 'workshop_data/plan/warehouse/enter_detail_in_form.html'
    form_class = ViewWarehouseRecordForm
    # success_url = reverse_lazy('all_record_in_warehouse')

    def form_valid(self, form):
        self.form = form
        return super(ViewWarehouseRecord, self).form_valid(form)

    def get_success_url(self):
        detail = self.form.cleaned_data['detail']
        product = self.form.cleaned_data['product']
        return reverse_lazy('all_record_in_warehouse', kwargs={'product': product,
                                                               'detail': detail})

