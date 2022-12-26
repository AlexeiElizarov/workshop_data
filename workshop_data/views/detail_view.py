import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from workshop_data.forms import AddImageInDetailForm, DetailCreateForm
from workshop_data.models import Detail
from ..filters import DetailFilter


class DetailAllView(LoginRequiredMixin, ListView):
    """Отображает страницу со всеми Деталями"""
    model = Detail
    template_name = 'workshop_data/detail/detail_list_all.html'
    context_object_name = 'details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filter'] = DetailFilter(self.request.GET, queryset=self.get_queryset())
        return context


class DetailCreateView(LoginRequiredMixin, CreateView):
    """Отображает страницу создания новой Детали"""
    model = Detail
    form_class = DetailCreateForm
    template_name = 'workshop_data/detail/detail_create.html'
    success_url = reverse_lazy('create_new_detail_complete')

    def post(self, request, *args, **kwargs):
        new_detail = super(DetailCreateView, self).post(request, *args, **kwargs)
        if "save_and_continue" in request.POST:
            new_detail = HttpResponseRedirect(reverse('create_new_detail'))
            time.sleep(1)
        return new_detail


class DetailDeleteView(LoginRequiredMixin, DeleteView):
    """Вьюха удаления Детали"""
    model = Detail
    template_name = 'workshop_data/detail/detail_delete.html'
    success_url = reverse_lazy('detail_list_all')

    def get_object(self, queryset=None):
        return Detail.objects.get(id=self.kwargs.pop('id'))


class AddImageInDetailView(LoginRequiredMixin, UpdateView):
    """Вьюха добавления Image в Деталь"""
    model = Detail
    form_class = AddImageInDetailForm
    template_name = 'workshop_data/detail/add_image_in_detail.html'
    success_url = reverse_lazy('detail_list_all')

    def get_object(self, queryset=None):
        return Detail.objects.get(name=self.kwargs.pop('detail'))


class DetailImageView(DetailView):
    """Просмотр изображения Детали"""
    model = Detail
    template_name = 'workshop_data/detail/image_detail.html'
    context_object_name = 'detail'

    def get_object(self, queryset=None):
        return Detail.objects.get(name=self.kwargs.get('pk'))

