import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, Avg
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView

from sign.forms import User
from workshop_data.filters import RecordJobFilter
from workshop_data.models import Product
from workshop_data.models.record_job import RecordJob, EvaluationOfTheOperatorsWork, ID_OPERATORS
from workshop_data.forms.record_job_form import (
    RecordJobForm,
    ParametersDetailForSPUCreateForm,
    MillingDetailForSPUCreateForm,
    EnteringOperatorWorkTimeForm,
    AverageCoefficientOperatorsForRangeDateForm
)
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from workshop_data.models.detail import ParametersDetailForSPU, Detail, Prefix, MillingDetailForSPU
from workshop_data.services import return_sum_recordjob_every_detail, counter_norm, return_detail_by_product_detail, \
    return_quantity_for_order, return_quantity_for_records
from workshop_data.services.evaluation_work_time import get_average_coefficient_all_operator, \
    update_database_after_deleting_record_work_time, get_average_coefficient_operator_range_date


class RecordJobCreateView(LoginRequiredMixin, CreateView):
    """Отображает страницу создания новой записи о сделанных за день деталей"""
    model = RecordJob
    form_class = RecordJobForm
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
            print()
            return HttpResponseRedirect(reverse_lazy('all_record_job'))


class RecordJobEditView(LoginRequiredMixin, UpdateView):
    """Отображает страницу редактирования записи о сделанных за день деталей"""
    model = RecordJob
    form_class = RecordJobForm
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
        print()
        print('********', self.kwargs)
        print()
        context['filter'] = RecordJobFilter(
            self.request.GET,
            queryset=self.get_queryset().order_by('-date').select_related('user',
                                                                          'detail',
                                                                          'product',
                                                                          'detail__prefix',
                                                                          'detail__parameters_for_spu'
                                                                          ).prefetch_related('detail__milling_in_detail'))
        if 'filter' in context:
            try:
                if 'month' in context['filter'].data and 'detail' in context['filter'].data:
                    detail = context['filter'].data['detail']
                    month = context['filter'].data['month']
                    records = RecordJob.objects.all().filter(detail=detail, month=month)
                    context['total_quantity'] = return_quantity_for_records(records)
                    context['month'] = month
                    context['detail'] = Detail.objects.get(id=detail)
                elif 'month' in context['filter'].data:
                    month = context['filter'].data['month']
                    records = RecordJob.objects.all().filter(month=month)
                    context['total_quantity'] = return_quantity_for_records(records)
                    context['month'] = month
                elif 'detail' in context['filter'].data:
                    detail=context['filter'].data['detail']
                    records = RecordJob.objects.all().filter(detail=detail)
                    context['total_quantity'] = return_quantity_for_records(records)
                    context['detail'] = Detail.objects.get(id=detail)
            except:
                return print('record_job_view.py 119')

        if 'month' in self.kwargs:
            context['records'] = RecordJob.objects.filter(month=self.kwargs['month']).order_by('-date')
        elif 'id' in self.kwargs:
            context['records'] = RecordJob.objects.filter(user=User.objects.get(id=self.kwargs.get('id'))).order_by('-date')
        elif 'product' in self.kwargs:
            context['records'] = RecordJob.objects.filter(product=Product.objects.get(name=self.kwargs.get('product')))
        elif 'detail' in self.kwargs:
            context['records'] = RecordJob.objects.filter(detail=Detail.objects.get(
                name=self.kwargs.get('detail').split('.')[1]))
        if 'records' in context:
            context['records'] = context['records'].order_by('-date').select_related('user',
                                                                                     'detail',
                                                                                     'product',
                                                                                     'detail__prefix',
                                                                                     'detail__parameters_for_spu'
                                                                                     ).prefetch_related(
                'detail__milling_in_detail')
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

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
                price=self.object.price if self.object.price is not None else 0,
                norm=self.object.norm if self.object.norm is not None else 0,
                difficultly=self.object.difficultly if self.object.difficultly is not None else 1,
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
        print(self.kwargs)
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


class MillingDetailForSPUCreateView(LoginRequiredMixin, CreateView):
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


class EnteringOperatorWorkTimeView(LoginRequiredMixin, CreateView):
    """Отображает страницу заполнения формы оценки работы оператора"""
    model = EvaluationOfTheOperatorsWork
    form_class = EnteringOperatorWorkTimeForm
    template_name = 'workshop_data/record_job/evaluation_work/evaluation_operator_work.html'
    success_url = reverse_lazy('all_operators_time')


class EditOperatorWorkTimeView(LoginRequiredMixin, UpdateView):
    """Редактирование записи работы оператора"""
    model = EvaluationOfTheOperatorsWork
    form_class = EnteringOperatorWorkTimeForm
    template_name = 'workshop_data/record_job/evaluation_work/evaluation_operator_work.html'
    success_url = reverse_lazy('all_operators_time')

    def get_object(self, queryset=None):
        return EvaluationOfTheOperatorsWork.objects.get(id=self.kwargs.get('id'))


class DeletingOperatorWorkTimeView(LoginRequiredMixin, DeleteView):
    """Отображает страницу удаления записи работы оператора"""
    model = EvaluationOfTheOperatorsWork
    template_name = 'workshop_data/record_job/evaluation_work/delete_record_operator_work_time.html'
    success_url = reverse_lazy('all_operators_time')

    def get_object(self, queryset=None):
        return EvaluationOfTheOperatorsWork.objects.get(id=self.kwargs.get('id'))

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        update_database_after_deleting_record_work_time(self.kwargs.get('worker'), self.kwargs.get('date'))
        return HttpResponseRedirect(success_url)


class AllOperatorWorkTimeView(LoginRequiredMixin, ListView):
    """Отображает страницу с данными по отработанному времени операторов в смене"""
    model = EvaluationOfTheOperatorsWork
    template_name = 'workshop_data/record_job/evaluation_work/all_operator_work_time.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_records'] = (EvaluationOfTheOperatorsWork.objects.all().order_by('-date').
                                   select_related('worker',))
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        get_average_coefficient_all_operator(request)
        return render(request, self.template_name, context)


class AverageCoefficientOperators(LoginRequiredMixin, ListView):
    model = User
    template_name = 'workshop_data/record_job/evaluation_work/average_operators_coefficient.html'
    success_url = reverse_lazy('all_operators_time')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AverageCoefficientOperatorsForRangeDateForm
        context['operators'] = User.objects.filter(id__in=ID_OPERATORS)
        context['avg_range'] = self.request.session.get('dict_avg_range')
        context['date1'] = self.request.session.get('date1')
        context['date2'] = self.request.session.get('date2')
        context['data'] = \
            [
                {'name': user.get_full_name(),
                 'coefficient': user.average_coefficient_operator
                 } for user in User.objects.filter(id__in=ID_OPERATORS)
            ]
        if ('date1' in context and context['date1'] is not None) and ('date2' in context and context['date2'] is not None):
            context['data'] = \
                [
                    {'name': user,
                     'coefficient': coef[0]
                     } for user, coef in get_average_coefficient_operator_range_date(
                    self.request.session.get('date1'), self.request.session.get('date2')).items()
                ]
        return context

    def post(self, request):
        if request.method == 'POST':
            form = AverageCoefficientOperatorsForRangeDateForm(request.POST)
            if form.is_valid():
                date1 = form.cleaned_data['date1']
                date2 = form.cleaned_data['date2']
                avg_coefficient_operator_dict = get_average_coefficient_operator_range_date(date1, date2)
                sum_avg_coef = sum(sum(avg_coefficient_operator_dict.values(), []))
                if form.cleaned_data['salary'] is not None:
                    total_salary = float(form.cleaned_data['salary'])
                    request.session['total_salary'] = total_salary
                    for operator_id in ID_OPERATORS:
                        worker = User.objects.get(id=operator_id)
                        salary = int(total_salary / sum_avg_coef * avg_coefficient_operator_dict[worker.get_full_name()][0])
                        avg_coefficient_operator_dict[worker.get_full_name()].append(salary)
                request.session['dict_avg_range'] = avg_coefficient_operator_dict
                request.session['date1'] = str(date1)
                request.session['date2'] = str(date2)
                get_average_coefficient_all_operator(request)
                return redirect('average_coefficient_operators')
            else:
                form = AverageCoefficientOperatorsForRangeDateForm()
                return redirect('average_coefficient_operators')
        return redirect('all_operators_time')

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if 'dict_avg_range' in self.request.session:
            del self.request.session['dict_avg_range']
        if 'total_salary' in self.request.session:
            del self.request.session['total_salary']
        if 'date1' in self.request.session:
            del self.request.session['date1']
        if 'date2' in self.request.session:
            del self.request.session['date2']
        return render(request, self.template_name, context)


class DiagramWorkSPUView(LoginRequiredMixin, ListView):
    """Отображает диаграмму эффективности операторов"""
    model = RecordJob
    template_name = 'workshop_data/record_job/diagram_work_operators.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = RecordJobFilter(
            self.request.GET,
            queryset=self.get_queryset())
        # context['data'] = \
        # [
        #     {'name': user.surname,
        #      'norm': (RecordJob.objects.filter(user=user).aggregate(value=Sum(F('detail__parameters_for_spu__norm') * F('quantity'))))
        #      } for user in User.objects.filter(id__in=[62, 64, 75, 76])
        # ]
        if 'month' in self.request.GET:
            context['data'] = \
                [
                    {'name': user.surname,
                     'norm': counter_norm(month=self.request.GET['month'], worker=user)
                     } for user in User.objects.filter(id__in=ID_OPERATORS)
                ]
        return context


class DiagramWorkTimeOperatorView(LoginRequiredMixin, ListView):
    """Отображает диаграмму эффективности операторов"""
    model = EvaluationOfTheOperatorsWork
    template_name = 'workshop_data/record_job/evaluation_work/diagram_work_time_operator.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = RecordJobFilter(
            self.request.GET,
            queryset=self.get_queryset())
        # context['data'] = \
        # [
        #     {'name': user.surname,
        #      'norm': (RecordJob.objects.filter(user=user).aggregate(value=Sum(F('detail__parameters_for_spu__norm') * F('quantity'))))
        #      } for user in User.objects.filter(id__in=[62, 64, 75, 76])
        # ]
        context['data'] = \
            [
                {'name': user.get_full_name(),
                 'coefficient': user.average_coefficient_operator
                 } for user in User.objects.filter(id__in=ID_OPERATORS)
            ]
        print()
        print('********', context['data'])
        print()
        if 'month' in self.request.GET:
            context['data'] = \
                [
                    {'name': user.surname,
                     'coefficient': user.average_coefficient_operator
                     } for user in User.objects.filter(id__in=ID_OPERATORS)
                ]
        return context
