import time
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from workshop_data.models import Product, Detail
from workshop_data.filters import ProductFilter
from workshop_data.forms import ProductCreateForm, ProductAddDetailForm


class ProductAllView(LoginRequiredMixin, ListView):
    """Отображает страницу со всеми Изделиями"""
    model = Product
    template_name = 'workshop_data/product/product_list_all.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filter'] = ProductFilter(self.request.GET)
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Отображает страницу создания нового Изделия"""
    model = Product
    form_class = ProductCreateForm
    template_name = 'workshop_data/product/product_create.html'
    success_url = reverse_lazy('create_new_product_complete')

    def post(self, request, *args, **kwargs):
        new_product = super(ProductCreateView, self).post(request, *args, **kwargs)
        if "save_and_continue" in request.POST:
            new_product = HttpResponseRedirect(reverse('create_new_product'))
            time.sleep(1)
        return new_product

    def get_success_url(self):
        if "save_and_continue" in self.request.POST:
            return reverse('create_new_product')
        return super(ProductCreateView, self).get_success_url()


class ProductAddDetailView(LoginRequiredMixin, UpdateView):
    """Отображает страницу добавления Детали в Изделия"""
    model = Product
    form_class = ProductAddDetailForm
    template_name = 'workshop_data/product/product_add_detail.html'
    success_url = reverse_lazy('product_add_detail_complete')

    def get_object(self, **kwargs):
        obj = Product.objects.get(name=self.kwargs['product'])
        return obj

    # def get_initial(self):
    #     initial = super(ProductAddDetailView, self).get_initial()
    #     initial.update(
    #         {'name': self.get_object()}
    #     )
    #     return initial

    def form_valid(self, form):
        obj = self.get_object()
        form = self.form_class(self.request.POST)
        added_detail = Detail.objects.get(id=form.data['detail'])
        obj.detail.add(added_detail)
        if "save_and_continue" in self.request.POST:
            time.sleep(.5)
            return HttpResponseRedirect(reverse('product_add_detail', kwargs={'product': self.get_object()}))
        return redirect('product_add_detail_complete')


class ProductDataView(LoginRequiredMixin, DetailView):
    """Отображает Детали входящие в Изделие"""
    model = Product
    template_name = 'workshop_data/product/product_detail_view.html'

    def get_object(self, **kwargs):
        return Product.objects.get(name=self.kwargs.get('product'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['details'] = self.get_object().detail.select_related('category')
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Вьюха удаления Изделия"""
    model = Product
    template_name = 'workshop_data/product/delete_product.html'
    success_url = reverse_lazy('product_list_all')

    def get_object(self, queryset=None):
        name = self.kwargs.pop('product_name')
        obj = Product.objects.get(name=name)
        return obj


class DeleteDetailFromProductView(LoginRequiredMixin, DeleteView):
    """Удаление Детали из Изделия"""
    model = Product
    template_name = 'workshop_data/product/delete_detail_from_product.html'
    success_url = reverse_lazy('product_detail_data')

    def get_object(self, queryset=None):
        return Product.objects.get(name=self.kwargs.get('product'))

    def post(self, request, *args, **kwargs):
        detail = Detail.objects.get(name=self.kwargs.get('detail'))
        # detail = self.get_object()
        self.get_object().detail.remove(detail)
        return HttpResponseRedirect(reverse(
            'product_detail_data',
            kwargs={'product': self.get_object()}
        ))
