from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView
from ..filters import BatchFilter
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from workshop_data.models.workshop_plan import WorkshopPlan
from workshop_data.forms.batch_form import CreateBatchDetailInPlanForm
from workshop_data.models import Detail, Product
from ..services import current_month, current_year


class CreateBatchDetailInPlan(LoginRequiredMixin, CreateView):
    """Запуск в производство новой партии Деталей"""
    model = BatchDetailInPlan
    form_class = CreateBatchDetailInPlanForm
    template_name = 'workshop_data/master/batch/create_batch_in_plan.html'

    def get_object(self, queryset=None):
        name = self.kwargs.get('product')
        product = name.split('_')[0]
        detail = name.split('_')[1]
        obj = WorkshopPlan.objects.get(product__name=product, detail__name=detail)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_detail'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy('batchs_in_plan', kwargs=({'object': self.get_object()}))

    def get_form_kwargs(self):
        kwargs = super(CreateBatchDetailInPlan, self).get_form_kwargs()
        kwargs.update({'object': self.kwargs.get('product')})
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        batch = form.save(commit=False)
        batch.author = self.request.user
        batch.detail = self.get_object().detail
        batch.save()
        batch.workshopplan_detail.save()
        return HttpResponseRedirect(reverse_lazy('batchs_in_plan',kwargs=({'object': self.get_object()})))


class AllBatchDetailInPlanView(LoginRequiredMixin, ListView):
    """Отображает все партии Деталей"""
    model = BatchDetailInPlan
    template_name = 'workshop_data/master/batch/all_batch_detail.html'
    ordering = ['workshopplan_detail']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filter'] = BatchFilter(self.request.GET, queryset=self.get_queryset())
        return context


# class DeleteBatchDetailInPlanView(LoginRequiredMixin, DeleteView):
#     """Удаляет Партию"""
#     model = BatchDetailInPlan
#     template_name = 'workshop_data/master/batch/batch_delete.html'
#
#     def get_object(self, queryset=None):
#         id = self.kwargs.get('id')
#         return BatchDetailInPlan.objects.get(pk=id)
#
#     def get_success_url(self):
#         return reverse_lazy('batchs_in_plan', kwargs=({'object': self.get_object().workshopplan_detail}))


class AllBatchDetailProductInPlan(LoginRequiredMixin, DetailView):
    """Отображает все Партии определённой Детали определённого Изделия"""
    model = BatchDetailInPlan
    template_name = 'workshop_data/master/batch/all_batch_detail_in_plan.html'

    def get_object(self, **kwargs):  # FIXME можно ли как то по-другому найти obj?
        name = self.kwargs.get('object')
        product = name.split('_')[0]
        detail = name.split('_')[1]
        obj = WorkshopPlan.objects.get(product__name=product, detail__name=detail)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['batchs_in_plan'] = BatchDetailInPlan.objects.filter(workshopplan_detail=self.get_object().id)
        context['filter'] = BatchFilter(self.request.GET, queryset=self.get_queryset())
        context['object'] = self.get_object()
        return context
