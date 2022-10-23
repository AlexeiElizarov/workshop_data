from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView

from ..filters import BatchFilter
from ..models import BatchDetailInPlan, WorkshopPlan
from ..forms import CreateBatchDetailInPlanForm
from ..services import get_quantity_detail_by_orders
from sign.models import User


class CreateBatchDetailInPlan(CreateView):
    '''Запуск в производсто новой партии Деталей'''
    model = BatchDetailInPlan
    form_class = CreateBatchDetailInPlanForm
    template_name = 'workshop_data/master/batch/create_batch_in_plan.html'
    success_url = reverse_lazy('product_add_plan_complite')

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

    def get_form_kwargs(self):
        kwargs = super(CreateBatchDetailInPlan, self).get_form_kwargs()
        kwargs.update({'object': self.kwargs.get('product')})
        return kwargs

    def get_quantity_detail_in_work(self):
        detail = BatchDetailInPlan.objects.filter()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        # self.object.workshopplan_detail.in_work += self.object.quantity_in_batch
        self.object.workshopplan_detail.save()
        return HttpResponseRedirect(reverse_lazy('product_add_plan_complite'))


class AllBatchDetailInPlanView(ListView):
    '''Отображает все партии Деталей'''
    model = BatchDetailInPlan
    template_name = 'workshop_data/master/batch/all_batch_detail_in_plan.html'
    context_object_name = 'batchs_in_plan'
    ordering = ['workshopplan_detail']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filter'] = BatchFilter(self.request.GET, queryset=self.get_queryset())
        return context


class DeleteBatchDetailInPlanView(DeleteView):
    '''Удаляет Партию'''
    model = BatchDetailInPlan
    template_name = 'workshop_data/master/batch/batch_delete.html'
    success_url = reverse_lazy('all_batch_in_plan')

    # def get_success_url(self, **kwargs):
    #     return reverse("orders_user_list_all", kwargs={'username': self.kwargs['username']})

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return BatchDetailInPlan.objects.get(pk=id)

    def form_valid(self, form):
        workshopplan_object = WorkshopPlan.objects.get(batchs=self.kwargs.get('id'))
        batch = self.get_object()
        # workshopplan_object.in_work -= batch.quantity_in_batch
        workshopplan_object.save()
        return super(DeleteBatchDetailInPlanView, self).form_valid(self)


class AllBatchDetailProductInPlan(DetailView):
    '''Отображает все Партии определённой Детали определённого Изделия'''
    model = BatchDetailInPlan
    template_name = 'workshop_data/master/batch/all_batch_detail_in_plan.html'
    context_object_name = 'batchs_in_plan'

    def get_object(self, **kwargs):  # FIXME можно ли как то по-другому найти obj?
        name = self.kwargs.get('object')
        product = name.split('_')[0]
        detail = name.split('_')[1]
        obj = WorkshopPlan.objects.get(product__name=product, detail__name=detail)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['batchs_in_plan'] = BatchDetailInPlan.objects.filter(workshopplan_detail=self.get_object().id)
        context['object'] = self.get_object()
        return context