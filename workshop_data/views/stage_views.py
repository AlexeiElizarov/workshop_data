import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from ..models import StageManufacturingDetailInWork, StageManufacturingDetail, BatchDetailInPlan, Order
from ..forms import CreateNewStageManufacturingInWorkForm, EditStageInDetail, AddStageInDeatailForm


class StageManufacturingDetailInWorkInPlanView(DetailView):
    '''Все Этапы производства определенной Партии'''
    model = StageManufacturingDetailInWork
    template_name = 'workshop_data/master/stage_in_work/all_stage_batch_in_work.html'

    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return id

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['stages'] = StageManufacturingDetailInWork.objects.filter(batch_id=self.kwargs.get('id'))
        context['batch_id'] = self.kwargs.get('id')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()


class StageManufacturingDetailInWorkView(CreateView):
    '''Запуска в производство определенного Этапа изготовления Партии Детали'''
    model = StageManufacturingDetailInWork
    form_class = CreateNewStageManufacturingInWorkForm
    template_name = 'workshop_data/master/stage_in_work/start_new_stage_in_work.html'
    success_url = reverse_lazy('start_new_stage_in_work_complete')

    def get_object(self, queryset=None):
        batch_id = self.kwargs.get('batch')
        obj = BatchDetailInPlan.objects.get(id=batch_id)
        return obj

    def get_form_kwargs(self):
        kwargs = super(StageManufacturingDetailInWorkView, self).get_form_kwargs()
        kwargs.update({'batch': self.kwargs.get('batch')})
        kwargs.update(
            {'stages': StageManufacturingDetail.objects.filter(
                detail_id=self.get_object().detail.detail_id)}
        )
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        order_object = Order(
            date=datetime.datetime.now(),
            month=self.object.batch.detail.month,
            surname=self.object.worker,
            employee_number=self.object.worker.employee_number,
            product=self.object.batch.detail.product,
            detail=self.object.batch.detail.detail,
            operations=self.object.stage_in_batch,
            quantity=self.object.batch.quantity_in_batch,
            normalized_time=self.object.stage_in_batch.normalized_time,
            price=self.object.stage_in_batch.price
        )
        order_object.save()
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('start_new_stage_in_work_complete'))


class EditStageInDetailView(UpdateView):
    '''Отображает страницу редактирования Этапа в Детоли'''
    model = StageManufacturingDetail
    form_class = EditStageInDetail
    template_name = 'workshop_data/product/product_add_detail.html'
    success_url = reverse_lazy('product_add_detail_complite')

    def get_object(self, **kwargs):
        obj = StageManufacturingDetail.objects.get(id=self.kwargs['pk'])
        return obj


class StageInDetailView(DetailView):
    '''Просмотр всех Этапов производства Детали'''
    model = StageManufacturingDetail
    template_name = 'workshop_data/detail/stage/stage_in_detail_all.html'
    context_object_name = 'stages'

    def get_object(self, queryset=None):
        return StageManufacturingDetail.objects.filter(detail_id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stages'] = self.get_object()
        return context


class AddStageInDeatailVeiw(CreateView):
    '''Добавление Этапа к Детали'''
    model = StageManufacturingDetail
    form_class = AddStageInDeatailForm
    template_name = 'workshop_data/detail/stage/add_stage_in_detail.html'
    success_url = reverse_lazy('add_stage_in_detail_complite')

    # чтобы передать pk в форму
    def get_form_kwargs(self):
        kwargs = super(AddStageInDeatailVeiw, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs.get('pk')})
        return kwargs