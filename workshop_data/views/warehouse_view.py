from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView, ListView

from workshop_data.models import Warehouse, Detail
from workshop_data.forms.warehouse_form import WarehouseCreateForm
from workshop_data.models.detail import Prefix


class WarehouseCreateView(LoginRequiredMixin, CreateView):
    """Отображает внесение количества деталей в кладовой"""
    model = Warehouse
    form_class = WarehouseCreateForm
    template_name = 'workshop_data/plan/warehouse/warehouse.html'
    success_url = reverse_lazy('plan')

    def get_form_kwargs(self):
        kwargs = super(WarehouseCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        detail = Detail.objects.get(prefix=Prefix.objects.get(
            name=self.kwargs.get('object').split('_')[1].split('.')[0]
        ),
            name=self.kwargs.get('object').split('.')[1])
        detail.in_warehouse = self.object
        detail.save()
        self.object.author = self.request.user
        return super().form_valid(form)


class WarehouseUpdateView(LoginRequiredMixin, UpdateView):
    """Отображает изменения количества деталей в кладовой"""
    model = Warehouse
    form_class = WarehouseCreateForm
    template_name = 'workshop_data/plan/warehouse/warehouse.html'
    success_url = reverse_lazy('plan')

    def get_form_kwargs(self):
        kwargs = super(WarehouseUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_object(self, **kwargs):
        obj = Warehouse.objects.get(id=self.kwargs.get('object_id'))
        return obj
