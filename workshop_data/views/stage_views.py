import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, ListView, TemplateView, FormView

from workshop_data.filters import DetailFilter
from workshop_data.models import Detail
from workshop_data.models.stage_manufacturing_detail import StageManufacturingDetail
from workshop_data.models.stage_manufacturing_detail_in_work import StageManufacturingDetailInWork
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from workshop_data.forms import (
    CreateNewStageManufacturingInWorkForm,
    EditStageInDetailForm,
    AddStageInDetailForm,
    EnteringDetailToViewAverageTimeOfWorkForm)
from workshop_data.models.order import Order
from workshop_data.services import (
    get_list_locksmith,
    get_list_turner,
    get_list_miller,
    get_dict_worker_quantity_detail,
    get_average_time_of_work_stage_in_detail, get_not_work_stages_in_batch, get_batch_by_id)


class StageManufacturingDetailInWorkInPlanView(LoginRequiredMixin, DetailView):
    """Все Этапы производства определенной Партии"""
    model = StageManufacturingDetailInWork
    template_name = 'workshop_data/master/stage_in_work/all_stage_batch_in_work.html'

    def get_object(self, **kwargs):
        return BatchDetailInPlan.objects.get(id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        stages_in_work = StageManufacturingDetailInWork.objects.filter(batch_id=self.kwargs.get('id'))
        context['stages_in_work'] = stages_in_work
        context['batch_id'] = self.kwargs.get('id')
        context['stages'] = get_not_work_stages_in_batch(self.get_object())
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()


class StageManufacturingDetailInWorkView(LoginRequiredMixin, CreateView):
    """Запуск в производство определенного Этапа изготовления Партии Детали"""
    model = StageManufacturingDetailInWork
    form_class = CreateNewStageManufacturingInWorkForm
    template_name = 'workshop_data/master/stage_in_work/start_new_stage_in_work.html'
    success_url = reverse_lazy('start_new_stage_in_work_complete')

    # def get_object(self, queryset=None):
    #     batch_id = self.kwargs.get('batch')
    #     obj = BatchDetailInPlan.objects.filter(id=batch_id).\
    #         select_related('workshopplan_detail__detail','workshopplan_detail__product')
    #     return obj[0]

    def get_form_kwargs(self):
        kwargs = super(StageManufacturingDetailInWorkView, self).get_form_kwargs()
        kwargs.update({'batch': self.kwargs.get('batch')})
        kwargs.update(
            {'stages': StageManufacturingDetail.objects.filter(
                detail_id=
                get_batch_by_id(self.kwargs.get('batch')).workshopplan_detail.detail.id)}
        )
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        batch = get_batch_by_id(self.kwargs.get('batch'))
        wp_obj = batch.workshopplan_detail
        context['batch_id'] = batch.id
        context['stages_in_work'] = StageManufacturingDetailInWork.objects.filter(batch_id=batch.id)
        context['workers_quantity_lsm'] = \
            get_dict_worker_quantity_detail(wp_obj.product, wp_obj.detail, get_list_locksmith())
        context['workers_quantity_trn'] = \
            get_dict_worker_quantity_detail(wp_obj.product, wp_obj.detail, get_list_turner())
        context['workers_quantity_mlr'] = \
            get_dict_worker_quantity_detail(wp_obj.product, wp_obj.detail, get_list_miller())
        context['stages'] = get_not_work_stages_in_batch(batch)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        order_object = Order(
            date=datetime.datetime.now(),
            user=self.object.worker,
            employee_number=self.object.worker.employee_number,
            batch=self.get_batch(),
            product=self.object.batch.workshopplan_detail.product,
            detail=self.object.batch.workshopplan_detail.detail,
            operations=self.object.stage_in_batch,
            quantity=self.object.batch.quantity_in_batch,
            normalized_time=self.object.stage_in_batch.normalized_time,
            price=self.object.stage_in_batch.price,
            author=self.request.user
        )
        args = {'order': order_object}
        if 'view' in self.request.POST:
            return render(self.request, 'workshop_data/order_template_for_print.html', args)
        elif 'save' in self.request.POST:
            order_object.author = self.request.user
            order_object.save()
            self.object.author = self.request.user
            self.object.save()
            return HttpResponseRedirect(reverse_lazy('batchs_in_plan',
                                                     kwargs={'object': order_object.batch.workshopplan_detail}))

    def get_batch(self):
        return get_batch_by_id(self.kwargs.get('batch'))


class EditStageManufacturingDetailInWorkView(LoginRequiredMixin, UpdateView):
    """Отображает страницу редактирования запуска Этапа"""
    model = StageManufacturingDetailInWork
    form_class = CreateNewStageManufacturingInWorkForm
    template_name = 'workshop_data/master/stage_in_work/start_new_stage_in_work.html'
    success_url = reverse_lazy('start_new_stage_in_work_complete')

    def get_object(self, queryset=None):
        batch_id = self.kwargs.get('batch')
        obj = BatchDetailInPlan.objects.get(id=batch_id)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        wp_obj = self.get_object().workshopplan_detail
        context['workers_quantity_lsm'] = \
            get_dict_worker_quantity_detail(wp_obj.product, wp_obj.detail, get_list_locksmith())
        context['workers_quantity_trn'] = \
            get_dict_worker_quantity_detail(wp_obj.product, wp_obj.detail, get_list_turner())
        context['workers_quantity_mlr'] = \
            get_dict_worker_quantity_detail(wp_obj.product, wp_obj.detail, get_list_miller())
        return context

    def get_form_kwargs(self):
        kwargs = super(EditStageManufacturingDetailInWorkView, self).get_form_kwargs()
        kwargs.update({'batch': self.kwargs.get('batch')})
        kwargs.update(
            {'stages': StageManufacturingDetail.objects.filter(
                detail_id=self.get_object().workshopplan_detail.detail_id)}
        )
        kwargs.update({'last_stage_in_work': self.get_object().stages.all().last()})
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        wrong_order = Order.objects.get(
            batch=self.get_object(),
            operations=self.get_form_kwargs()['last_stage_in_work'].stage_in_batch
        )
        wrong_order.delete()
        wrong_stage_manufacturing_detail_in_work = \
            StageManufacturingDetailInWork.objects.get(batch=self.object)
        wrong_stage_manufacturing_detail_in_work.delete()
        order_object = Order(
            date=datetime.datetime.now(),
            month=self.object.workshopplan_detail.month,
            user=form.cleaned_data['worker'],
            employee_number=form.cleaned_data['worker'].employee_number,
            batch=self.object,
            product=self.object.workshopplan_detail.product,
            detail=self.object.workshopplan_detail.detail,
            operations=form.cleaned_data['stage_in_batch'],
            quantity=self.object.quantity_in_batch,
            normalized_time=form.cleaned_data['stage_in_batch'].normalized_time,
            price=form.cleaned_data['stage_in_batch'].price,
            author=self.request.user
        )
        order_object.save()
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('start_new_stage_in_work_complete'))


class EditStageInDetailView(LoginRequiredMixin, UpdateView):
    """Отображает страницу редактирования Этапа в Детали"""
    model = StageManufacturingDetail
    form_class = EditStageInDetailForm
    template_name = 'workshop_data/product/product_add_detail.html'
    success_url = reverse_lazy('product_add_detail_complete')

    def get_object(self, **kwargs):
        obj = StageManufacturingDetail.objects.get(id=self.kwargs['pk'])
        return obj


class StageInDetailView(LoginRequiredMixin, DetailView):
    """Просмотр всех Этапов производства Детали"""
    model = StageManufacturingDetail
    template_name = 'workshop_data/detail/stage/stage_in_detail_all.html'
    context_object_name = 'stages'

    def get_object(self, queryset=None):
        if 'detail' in self.kwargs:
            return StageManufacturingDetail.objects.filter(detail_id=self.kwargs.get('pk'))
        elif 'node' in self.kwargs:
            return StageManufacturingDetail.objects.filter(node_id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'detail' in self.kwargs:
            context['detail'] = Detail.objects.get(id=self.kwargs.get('pk'))
        return context


class AddStageInDeatailVeiw(LoginRequiredMixin, CreateView):
    """Добавление Этапа к Детали"""
    model = StageManufacturingDetail
    form_class = AddStageInDetailForm
    template_name = 'workshop_data/detail/stage/add_stage_in_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'detail_id' in self.kwargs:
            context['stages'] = StageManufacturingDetail.objects.filter(detail_id=self.kwargs.get('detail_id'))
        elif 'node_id' in self.kwargs:
            context['stages'] = StageManufacturingDetail.objects.filter(node_id=self.kwargs.get('node_id'))
        return context

    # чтобы передать pk в форму
    def get_form_kwargs(self):
        kwargs = super(AddStageInDeatailVeiw, self).get_form_kwargs()
        if self.kwargs.get('detail_id'):
            kwargs.update({'detail_id': self.kwargs.get('detail_id')})
        elif self.kwargs.get('node_id'):
            kwargs.update({'node_id': self.kwargs.get('node_id')})
        return kwargs

    def form_valid(self, form):
        form = form.save()
        if self.kwargs.get('detail_id'):
            return HttpResponseRedirect(reverse_lazy(
                'all_stage_in_detail', kwargs={'pk': self.kwargs.get('detail_id'),
                                               'detail': self.kwargs.get('detail')}))
        elif self.kwargs.get('node_id'):
            return HttpResponseRedirect(reverse_lazy(
                'all_stage_in_node', kwargs={'pk': self.kwargs.get('node_id'),
                                             'node': self.kwargs.get('node')}))


class EnteringDetailToViewAverageTimeOfWorkView(FormView):
    """Ввод детали для отображения таблицы среднего времени работы над этапом детали"""
    model = StageManufacturingDetailInWork
    form_class = EnteringDetailToViewAverageTimeOfWorkForm
    template_name = 'workshop_data/master/stage_in_work/average_time_of_work_stage_in_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = DetailFilter(self.request.GET)
        if 'detail' in self.kwargs:
            context['stages_in_detail'] = get_average_time_of_work_stage_in_detail(self.kwargs['detail'])
        if 'quantity_detail' in self.kwargs:
            context['quantity_detail'] = self.kwargs.get('quantity_detail')
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            detail = Detail.objects.get(id=form.cleaned_data['name'])
            quantity_detail = form.cleaned_data['quantity_detail']
            if detail and quantity_detail:
                return HttpResponseRedirect(reverse_lazy('average_time_of_work_stage_in_detail_2_parameter',
                                                  kwargs={'detail': detail.name,
                                                          'quantity_detail': quantity_detail}))
            if detail:
                return HttpResponseRedirect(reverse_lazy('average_time_of_work_stage_in_detail_1_parameter',
                                                         kwargs={'detail': detail.name,
                                                                 }))
        return HttpResponseRedirect(reverse_lazy('average_time_of_work_stage_in_detail'))


class AverageTimeOfWorkStageInDetailView(ListView):
    """Таблица среднего времени работы над этапом детали"""

    model = StageManufacturingDetail
    template_name = 'workshop_data/master/stage_in_work/average_time_of_work_stage_in_detail.html'


