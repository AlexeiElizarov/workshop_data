import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from workshop_data.models.stage_manufacturing_detail import StageManufacturingDetail
from workshop_data.models.stage_manufacturing_detail_in_work import StageManufacturingDetailInWork
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from workshop_data.forms import (
    CreateNewStageManufacturingInWorkForm,
    EditStageInDetailForm,
    AddStageInDeatailForm)
from workshop_data.models.order import Order
from workshop_data.services import (
    get_list_locksmith,
    get_list_turner,
    get_list_miller,
    get_dict_worker_quantity_detail)


class StageManufacturingDetailInWorkInPlanView(DetailView):
    '''Все Этапы производства определенной Партии'''
    model = StageManufacturingDetailInWork
    template_name = 'workshop_data/master/stage_in_work/all_stage_batch_in_work.html'

    def get_object(self, **kwargs):
        return BatchDetailInPlan.objects.get(id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        stages_in_work = StageManufacturingDetailInWork.objects.filter(batch_id=self.kwargs.get('id'))
        context['stages_in_work'] = stages_in_work
        context['batch_id'] = self.kwargs.get('id')
        stages = self.get_object().workshopplan_detail.detail.stages.all()
        not_work_stages = []
        for i in range(len(stages_in_work), len(stages)):
            not_work_stages.append(stages[i])
        context['stages'] = not_work_stages
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
                detail_id=self.get_object().workshopplan_detail.detail_id)}
        )
        kwargs.update({'user': self.request.user})
        return kwargs

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

    def form_valid(self,  form):
        self.object = form.save(commit=False)
        # self.request.session['form'] = self.object
        order_object = Order(
            date=datetime.datetime.now(),
            user=self.object.worker,
            employee_number=self.object.worker.employee_number,
            batch=self.get_object(),
            product=self.object.batch.workshopplan_detail.product,
            detail=self.object.batch.workshopplan_detail.detail,
            operations=self.object.stage_in_batch,
            quantity=self.object.batch.quantity_in_batch,
            normalized_time=self.object.stage_in_batch.normalized_time,
            price=self.object.stage_in_batch.price,
            author=self.request.user
        )
        args = {}
        args['order'] = order_object
        if 'view' in self.request.POST:
            return render(self.request, 'workshop_data/test.html', args)
        elif 'save' in self.request.POST:
            order_object.save()
            self.object.author = self.request.user
            self.object.save()
            return HttpResponseRedirect(reverse_lazy('start_new_stage_in_work_complete'))


class EditStageManufacturingDetailInWorkView(UpdateView):
    '''Отображает страницу редактирования запуска Этапа'''
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
            operations=form.cleaned_data['stage_in_batch']
        )
        wrong_order.delete()
        wrong_stage_manufacturing_detail_in_work = \
            StageManufacturingDetailInWork.objects.get(batch=self.object)
        wrong_stage_manufacturing_detail_in_work.delete()
        order_object = Order(
            date=datetime.datetime.now(),
            month=self.object.workshopplan_detail.month,
            surname=form.cleaned_data['worker'],
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


class EditStageInDetailView(UpdateView):
    '''Отображает страницу редактирования Этапа в Детали'''
    model = StageManufacturingDetail
    form_class = EditStageInDetailForm
    template_name = 'workshop_data/product/product_add_detail.html'
    success_url = reverse_lazy('product_add_detail_complite')

    def get_object(self, **kwargs):
        obj = StageManufacturingDetailInWork.objects.get(id=self.kwargs['pk'])
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