import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView

from sign.forms import User
from workshop_data.filters import RecordJobFilter
from workshop_data.models import Product
from workshop_data.models.record_job import RecordJob
from workshop_data.forms.record_job_form import (
    RecordJobForm,
    ParametersDetailForSPUCreateForm,
    MillingDetailForSPUCreateForm,
)
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from workshop_data.models.detail import ParametersDetailForSPU, Detail, Prefix, MillingDetailForSPU
from workshop_data.services import return_sum_recordjob_every_detail, counter_norm, return_detail_by_product_detail


class RecordJobCreateView(LoginRequiredMixin, CreateView):
    """Отображает страницу создания новой записи о сделанных за день деталей"""
    model = RecordJob
    form_class = RecordJobForm
    login_url = '/login/'
    template_name = 'workshop_data/record_job/create_record_job.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.is_valid():
            record_job = RecordJob(
                date=datetime.datetime.now(),
                month=self.object.month,
                user=self.object.user,
                product=self.object.product,
                detail=self.object.detail,
                quantity_1=self.object.quantity_1 if self.object.quantity_1 else 0,
                quantity_2=self.object.quantity_2 if self.object.quantity_2 else 0,
                quantity=self.object.quantity if self.object.quantity else 0,
                milling_was=self.object.milling_was,
                author_id=self.request.user.id
            )
            record_job.save()
            return HttpResponseRedirect(reverse_lazy('all_record_job'))


class RecordJobEditView(LoginRequiredMixin, UpdateView):
    """Отображает страницу редактирования записи о сделанных за день деталей"""
    model = RecordJob
    form_class = RecordJobForm
    login_url = '/login/'
    template_name = 'workshop_data/record_job/create_record_job.html'

    def get_object(self, queryset=None):
        print(self.kwargs)
        obj = RecordJob.objects.get(
            id=self.kwargs.get('id')
        )
        return obj

    def get_success_url(self):
        print(self.kwargs)
        return reverse('all_record_job')


class RecordJobDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление записи о сделанных за день деталей"""
    model = RecordJob
    template_name = 'workshop_data/record_job/record_job_delete.html'
    success_url = reverse_lazy('all_record_job')

    def get_object(self, queryset=None):
        return RecordJob.objects.get(id=self.kwargs.get('id'))


class AllRecordJobForAllWorker(LoginRequiredMixin, ListView):
    """Отображает все записи о сделанных за день деталей"""
    model = RecordJob
    template_name = 'workshop_data/record_job/all_records_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['records'] = RecordJob.objects.all().select_related('product',
        #                                                             'detail',
        #                                                             'detail__prefix',
        #                                                             'detail__parameters_for_spu',
        #                                                             'user',
        #                                                             )
        context['filter'] = RecordJobFilter(
            self.request.GET,
            queryset=self.get_queryset().select_related('user',
                                                        'detail',
                                                        'product',
                                                        'detail__prefix',
                                                        'detail__parameters_for_spu',
                                                        ))
        if 'month' in self.kwargs:
            context['records'] = RecordJob.objects.filter(month=self.kwargs['month']).order_by('date')
        elif 'username' in self.kwargs:
            context['records'] = RecordJob.objects.filter(user=User.objects.get(username=self.kwargs.get('username')))
        elif 'product' in self.kwargs:
            context['records'] = RecordJob.objects.filter(product=Product.objects.get(name=self.kwargs.get('product')))
        elif 'detail' in self.kwargs:
            context['records'] = RecordJob.objects.filter(detail=Detail.objects.get(
                name=self.kwargs.get('detail').split('.')[1]))
        if 'records' in context:
            context['records'] = context['records'].select_related('user',
                                                                   'detail',
                                                                   'product',
                                                                   'detail__prefix',
                                                                   'detail__parameters_for_spu',
                                                                   ).prefetch_related('detail__millingdetailforspu_set')
        return context


class AllRecordJobForWorker(LoginRequiredMixin, ListView):
    """Отображает все записи рабочего о сделанных за день деталей"""
    model = RecordJob
    template_name = 'workshop_data/record_job/all_records_for_worker.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = User.objects.get(id=self.kwargs.get('id'))
        context['worker'] = worker
        context['records'] = RecordJob.objects.filter(user=worker.id) \
            .select_related('product',
                            'detail',
                            'detail__prefix',
                            'detail__parameters_for_spu',
                            'user',
                            )
        if 'month' in self.kwargs:
            context['records'] = RecordJob.objects.filter(
                month=self.kwargs['month'],
                user=worker).order_by('date')
            context['salary_per_month'] = 0
            context['month'] = self.kwargs.get('month')
        return context


class AllRecordJobForWorkerPerMonth(LoginRequiredMixin, ListView):
    """Отображает все записи рабочего о сделанных за день деталей за месяц
        (и суммирует одинаковые детали)"""
    model = RecordJob
    template_name = 'workshop_data/record_job/all_records_for_worker_dict.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = User.objects.get(id=self.kwargs.get('id'))
        context['worker'] = worker
        if 'month' in self.kwargs:
            month = self.kwargs.get('month')
            records = RecordJob.objects.filter(
                month=month,
                user=worker).order_by('date')
            context['records'] = records
            context['salary_per_month'] = 0
            context['month'] = month
            context['qqq'] = return_sum_recordjob_every_detail(records)
        return context


class ParametersDetailForSPUCreateView(LoginRequiredMixin, CreateView):
    """Заполнение параметров детали на участке СПУ"""
    model = ParametersDetailForSPU
    form_class = ParametersDetailForSPUCreateForm
    template_name = 'workshop_data/record_job/parameter_detail_for_spu_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        data = self.kwargs.get('detail').split('.')
        if len(data) > 1:
            detail = Detail.objects.get(name=data[1],
                                        prefix=Prefix.objects.get(name=data[0]))
        else:
            detail = Detail.objects.get(name=data[0])
        if form.is_valid():
            if detail.parameters_for_spu:
                detail.parameters_for_spu.delete()
            parameter_detail = ParametersDetailForSPU(
                operations_first_side=self.object.operations_first_side,
                operations_second_side=self.object.operations_second_side,
                first_side_time=self.object.first_side_time if self.object.first_side_time is not None else 1,
                coefficient_first_side=self.object.coefficient_first_side if self.object.coefficient_first_side is not None else 1,
                second_side_time=self.object.second_side_time if self.object.second_side_time is not None else 1,
                coefficient_second_side=self.object.coefficient_second_side if self.object.coefficient_second_side is not None else 1,
                price=self.object.price,
                norm=self.object.norm,
                author_id=self.request.user.id
            )
            parameter_detail.save()
            detail.parameters_for_spu = parameter_detail
            detail.save()
            return HttpResponseRedirect(reverse_lazy('edit_parameter_detail_spu',
                                                     kwargs={'product': self.kwargs.get('product'),
                                                             'detail': self.kwargs.get('detail')}))


class ParametersDetailForSPEditeView(LoginRequiredMixin, UpdateView):
    """Вьюха редактирования параметров СПУ"""
    model = ParametersDetailForSPU
    form_class = ParametersDetailForSPUCreateForm
    template_name = 'workshop_data/record_job/parameter_detail_for_spu_create.html'

    def get_object(self, queryset=None):
        data = self.kwargs.get('detail').split('.')
        if len(data) > 1:
            obj = ParametersDetailForSPU.objects.get(
                detail=Detail.objects.get(name=data[1],
                                          prefix=Prefix.objects.get(name=data[0]))
            )
        else:
            obj = ParametersDetailForSPU.objects.get(detail=Detail.objects.get(name=data[0]))
        return obj

    def get_success_url(self):
        return reverse('edit_parameter_detail_spu', kwargs={'product': self.kwargs.get('product'),
                                                            'detail': self.kwargs.get('detail')})


class MillingDetailForSPUCreateView(CreateView):
    """Создание новой записи фрезерования детали на СПУ участке"""
    model = MillingDetailForSPU
    form_class = MillingDetailForSPUCreateForm
    template_name = 'workshop_data/record_job/milling_detail_for_cpu_create.html'
    success_url = reverse_lazy('all_record_job')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        detail = return_detail_by_product_detail(self.kwargs.get('record'))
        milling = MillingDetailForSPU(
            name=self.object.name,
            time=self.object.time,
            norm_milling=self.object.norm_milling,
            price=self.object.price,
            operations=self.object.operations,
            milling_for_detail=detail,
        )
        milling.save()
        detail.parameters_for_spu.milling_operations = milling
        detail.parameters_for_spu.save()
        return HttpResponseRedirect(reverse_lazy('all_record_job'))


def parameters_detail_for_spu_create_or_edit_redirect(request, product, detail):
    obj = Detail.objects.get(name=detail.split('.')[1],
                             prefix=Prefix.objects.get(name=detail.split('.')[0]))
    if obj.parameters_for_spu:
        return redirect('edit_parameter_detail_spu', product=product, detail=detail)
    else:

        return redirect('create_parameter_detail_spu', product=product, detail=detail)


class DiagramWorkSPUView(LoginRequiredMixin, TemplateView):
    """Отображает диаграмму эффективности операторов"""
    model = RecordJob
    template_name = 'workshop_data/record_job/diagram_work_operators.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['data'] = \
        # [
        #     {'name': user.surname,
        #      'norm': (RecordJob.objects.filter(user=user).aggregate(value=Sum(F('detail__parameters_for_spu__norm') * F('quantity'))))
        #      } for user in User.objects.filter(id__in=[62, 64, 75, 76])
        # ]
        context['data'] = \
            [
                {'name': user.surname,
                 'norm': counter_norm(month='08', worker=user)
                 } for user in User.objects.filter(id__in=[43, 61])  # 43, 61 # 62, 64, 75, 76
            ]
        # context['fff'] = counter_norm()
        return context
