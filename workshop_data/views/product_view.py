from typing import Any

from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from ..models import Product, Detail
from ..filters import ProductFilter
from ..forms import ProductCreateForm, ProductAddDetailForm

class ProductAllView(ListView):
    '''Отображает страницу со всеми Изделиями'''
    model = Product
    template_name = 'workshop_data/product/product_list_all.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ProductCreateView(CreateView):
    '''Отображает страницу создания нового Изделия'''
    model = Product
    form_class = ProductCreateForm
    template_name = 'workshop_data/worker/product_create.html'
    success_url = reverse_lazy('create_new_product_complite')


class ProductAddDetailView(UpdateView):
    '''Отображает страницу добавления Детали в  Изделия'''
    model = Product
    form_class = ProductAddDetailForm
    template_name = 'workshop_data/product/product_add_detail.html'
    success_url = reverse_lazy('product_add_detail_complite')

    def get_object(self, **kwargs):
        obj = Product.objects.get(name=self.kwargs['product'])
        return obj

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> "HttpResponse":
        obj = self.get_object()
        if request.method == "POST":
            form = self.form_class(request.POST)
            detail_id = Detail.objects.get(id=form.data['detail'])
            obj.detail.add(detail_id)
        return redirect('product_add_detail_complite')


class ProductDataView(DetailView):
    model = Product
    template_name = 'workshop_data/product/product_detail_view.html'
    context_object_name = 'product'

    def get_object(self, **kwargs):
        id = Product.objects.get(name=self.kwargs.get('product')).id
        return Product.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['details'] = self.get_object().detail.all()
        return context

