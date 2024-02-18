from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView
from ..filters import BatchFilter
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from workshop_data.models.workshop_plan import WorkshopPlan
from workshop_data.forms.batch_form import CreateBatchDetailInPlanForm
from workshop_data.models import Detail, Product, StageManufacturingDetailInWork, Prefix
from ..services import current_month, current_year
from django.db.models import Prefetch


class CreateBatchDetailInPlan(LoginRequiredMixin, CreateView):
    """Запуск в производство новой партии Деталей"""
    model = BatchDetailInPlan
    form_class = CreateBatchDetailInPlanForm
    template_name = 'workshop_data/master/batch/create_batch_in_plan.html'

    def get_object(self, queryset=None):
        name = self.kwargs.get('object')
        prefix = name.split('_')[1].split('.')[0]
        detail_name = name.split('_')[1].split('.')[1]
        detail = Detail.objects.get(prefix__name=prefix, name=detail_name)

        product = name.split('_')[0]
        obj = WorkshopPlan.objects.filter(
            product__name=product,
            detail=detail).select_related('product', 'detail')[0]
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_detail'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy('batchs_in_plan', kwargs=({'object': self.get_object()}))

    def get_form_kwargs(self):
        kwargs = super(CreateBatchDetailInPlan, self).get_form_kwargs()
        kwargs.update({'object': self.kwargs.get('object')})
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        batch = form.save(commit=False)
        batch.author = self.request.user
        if self.get_object().detail:
            batch.detail = self.get_object().detail
        elif self.get_object().node:
            batch.node = self.get_object().node
        batch.workshopplan_detail = self.get_object()
        batch.save()
        # batch.workshopplan_detail.save()
        return HttpResponseRedirect(reverse_lazy('batchs_in_plan', kwargs=({'object': self.get_object()})))


class AllBatchDetailInPlanView(LoginRequiredMixin, ListView):
    """Отображает все партии Деталей"""
    model = BatchDetailInPlan
    template_name = 'workshop_data/master/batch/all_batch_detail.html'
    ordering = ['workshopplan_detail']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # context['batchs'] = BatchDetailInPlan.objects.\
        #     select_related('detail', 'workshopplan_detail', 'comment').\
        #     prefetch_related('detail__product').\
        #     prefetch_related(Prefetch('stages',
        #                               queryset=StageManufacturingDetailInWork.objects.
        #                               select_related('worker', 'stage_in_batch')))

        context['filter'] = BatchFilter(
            self.request.GET,
            queryset=self.get_queryset(). \
                select_related('detail', 'workshopplan_detail',). \
                prefetch_related('detail__detail_in_product'). \
                prefetch_related(Prefetch('stages',
                                          queryset=StageManufacturingDetailInWork.objects.
                                          select_related('worker', 'stage_in_batch'))))
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

    # def get_object(self, **kwargs):  # FIXME можно ли как то по-другому найти obj?
    #     name = self.kwargs.get('object')
    #     product = name.split('_')[0]
    #     detail = name.split('_')[1]
    #     obj = WorkshopPlan.objects.get(product__name=product, detail__name=detail)
    #     return obj

    def get_object(self, queryset=None):
        name = self.kwargs.get('object')

        # product = Product.objects.get(name=name.split('_')[0])
        # detail = Detail.objects.get(prefix=Prefix.objects.get(
        #     name=self.kwargs.get('object').split('_')[1].split('.')[0]
        # ),
        #     name=self.kwargs.get('object').split('_')[1].split('.')[1])

        prefix = name.split('_')[1].split('.')[0]
        detail_name = name.split('_')[1].split('.')[1]
        detail = Detail.objects.get(prefix__name=prefix, name=detail_name)

        product = name.split('_')[0]
        obj = WorkshopPlan.objects.filter(
            product__name=product,
            detail=detail).select_related('product', 'detail')[0]
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['batchs_in_plan'] = BatchDetailInPlan.objects.filter(workshopplan_detail=self.get_object().id)
        context['filter'] = BatchFilter(self.request.GET, queryset=self.get_queryset())
        context['object'] = self.get_object()
        return context
