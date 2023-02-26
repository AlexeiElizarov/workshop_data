import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from workshop_data.forms import CreateCategoryDetailForm
from workshop_data.models import CategoryDetail, Detail


class CreateCategoryDetailView(LoginRequiredMixin, CreateView):
    """Вьюха создания новой Категории"""
    model = CategoryDetail
    form_class = CreateCategoryDetailForm
    template_name = 'workshop_data/category_detail/create_new_category.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        if form.is_valid():
            new_category = CategoryDetail(
                name=form.cleaned_data.get('name'),
                author=self.request.user
            )
            new_category.save()
        if 'save_and_continue' in self.request.POST:
            time.sleep(1)
            return HttpResponseRedirect(reverse('create_new_category'))
        return HttpResponseRedirect(reverse_lazy('category_detail_all_list'))


class CategoryDetailAllList(LoginRequiredMixin, ListView):
    """Страница отображает все Категории Деталей"""
    model = CategoryDetail
    template_name = 'workshop_data/category_detail/category_detail_all_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_details'] = CategoryDetail.objects.all()
        # if 'category' in self.kwargs:
        #     category = CategoryDetail.objects.get(name=self.kwargs.get('category'))
        #     context['categories_details'] = Detail.objects.filter(category=category)
        return context


class CategoryDetailUpdateView(LoginRequiredMixin, UpdateView):
    """Вьюха редактирования категории"""
    form_class = CreateCategoryDetailForm
    template_name = 'workshop_data/category_detail/create_new_category.html'
    success_url = reverse_lazy('category_detail_all_list')

    def get_object(self, **kwargs):
        return CategoryDetail.objects.get(id=self.kwargs.get('id'))


class CategoryDetailDeleteView(DeleteView):
    """Вьюха удаления Категории"""
    model = CategoryDetail
    template_name = 'workshop_data/category_detail/delete_category_detail.html'
    success_url = reverse_lazy('category_detail_all_list')

    def get_object(self, queryset=None):
        return CategoryDetail.objects.get(id=self.kwargs.pop('id'))

