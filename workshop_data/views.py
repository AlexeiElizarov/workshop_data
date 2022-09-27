from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from dal import autocomplete
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import *
from .models import *
from sign.models import User
from django.utils.html import format_html
from django.db.models import Q
from .filters import *


def sum_parametrs(list_objects):
    '''Считает сумму зарплаты списка нарядов '''
    lst = []
    for obj in list_objects:
        salary = float(obj.price) * int(obj.quantity) * 1.4
        lst.append(salary)
    return sum(lst)


class WorkerAutocomplete(autocomplete.Select2QuerySetView):
    '''Реализует поле автоподсказки Рабочего по вводимыи символам'''

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(surname__istartswith=self.q)
        return qs


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    '''Реализует поле автоподсказки Изделий по вводимыи символам'''

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()
        qs = Product.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class DetailAutocomplete(autocomplete.Select2QuerySetView):
    '''Реализует поле автоподсказки Деталей по вводимыи символам'''

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Detail.objects.none()
        qs = Detail.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class CategoryDetailAutocomplete(autocomplete.Select2QuerySetView):
    '''Реализует поле автоподсказки Категории Деталей по вводимыи символам'''

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CategoryDetail.objects.none()
        qs = CategoryDetail.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class OrderUserCreateView(LoginRequiredMixin, CreateView):
    '''Отображает страницу заполнения нового наряда'''
    model = Order
    form_class = OrderForm
    template_name = 'workshop_data/worker/order_user_create_view.html'

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> "HttpResponse":
        form = self.form_class(request.POST)
        current_user = request.user
        if form.is_valid():
            order = Order(
                # date=request.POST['date'],
                month=form.cleaned_data['month'],
                # workshop=form.cleaned_data['workshop'],
                # section=form.cleaned_data['section'],
                surname_id=User.objects.get(username=current_user.username).id,
                employee_number=current_user.employee_number,
                product=form.cleaned_data['product'],
                detail=form.cleaned_data['detail'],
                operations=form.cleaned_data['operations'],
                quantity=form.cleaned_data['quantity'],
                normalized_time=form.cleaned_data['normalized_time'],
                price=form.cleaned_data['price'],
            )
            order.save()
        return redirect('orders_user_list_all', username=current_user.username)


class OrderUserParametrListView(LoginRequiredMixin, ListView):
    '''Отображает наряды пользователя фильтруя их в зависимости от переданного параметра'''
    model = Order
    login_url = '/login/'
    context_object_name = 'orders'
    template_name = 'workshop_data/worker/orders_user_parametr_list.html'

    def get_context_data(self, *args, **kwargs):
        print(self.request.user)
        user_id = User.objects.get(username=self.request.user.username).id
        context = super().get_context_data(**kwargs)
        if 'month' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id).filter(month=self.kwargs['month'])
            context['salary'] = sum_parametrs(context['orders'])
            context['month'] = context['orders'][0]
        elif 'product' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id). \
                filter(product_id=Product.objects.get(name=self.kwargs['product']))
        elif 'detail' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id). \
                filter(detail_id=Detail.objects.get(name=self.kwargs['detail']))
        elif 'category' in self.kwargs:
            context['orders'] = Order.objects.filter(surname_id=user_id). \
                filter(detail__category__name=self.kwargs['category'])
        else:
            context['orders'] = Order.objects.filter(surname_id=user_id)
        return context


class OrderUserEditView(LoginRequiredMixin, UpdateView):
    '''Редактирование наряда'''
    template_name = 'workshop_data/worker/order_user_create_view.html'
    form_class = OrderForm

    # success_url = reverse_lazy('orders_user_list_all') # FIXME    + git

    def get_success_url(self, **kwargs):
        return reverse("orders_user_list_all", kwargs={'username': self.kwargs['username']})

    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return Order.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderDeleteView(DeleteView):
    '''Удаление наряда'''
    template_name = 'workshop_data/worker/order_user_delete_view.html'
    queryset = Order.objects.all()

    def get_success_url(self, **kwargs):
        return reverse("orders_user_list_all", kwargs={'username': self.kwargs['username']})

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return Order.objects.get(pk=id)


##################### Product ####################################


class ProductAllView(ListView):
    '''Отображает страницу со всеми Изделиями'''
    model = Product
    template_name = 'workshop_data/product/product_list_all.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ProductCreateView(CreateView):
    '''Отображает страницу создания нового Изделия'''
    model = Product
    form_class = ProductCreateForm
    template_name = 'workshop_data/worker/product_create.html'
    success_url = reverse_lazy('create_new_product_complite')


class ProductAddDetailView(UpdateView):
    '''Отображает страницу добавления Детали в  Изделия'''
    model = Product
    form_class = ProductAddDetailForm
    template_name = 'workshop_data/product/product_add_detail.html'
    success_url = reverse_lazy('product_add_detail_complite')

    def get_object(self, **kwargs):
        obj = Product.objects.get(name=self.kwargs['product'])
        return obj

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> "HttpResponse":
        obj = self.get_object()
        if request.method == "POST":
            form = self.form_class(request.POST)
            detail_id = Detail.objects.get(id=form.data['detail'])
            obj.detail.add(detail_id)
        return redirect('product_add_detail_complite')


class ProductDataView(DetailView):
    model = Product
    template_name = 'workshop_data/product/product_detail_view.html'
    context_object_name = 'product'

    def get_object(self, **kwargs):
        id = Product.objects.get(name=self.kwargs.get('product')).id
        return Product.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['details'] = self.get_object().detail.all()
        return context


########################## Detail ##################################

class DetailAllView(ListView):
    '''Отображает страницу со всеми Деталями'''
    model = Detail
    template_name = 'workshop_data/detail/detail_list_all.html'
    context_object_name = 'details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filter'] = DetailFilter(self.request.GET, queryset=self.get_queryset())
        return context


class DetailCreateView(CreateView):
    '''Отображает страницу создания новоой Детали'''
    model = Detail
    form_class = DetailCreateForm
    template_name = 'workshop_data/detail/detail_create.html'
    success_url = reverse_lazy('create_new_detail_complite')


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


class EditStageInDetailView(UpdateView):
    '''Отображает страницу редактирования Этапа в Детоли'''
    model = StageManufacturingDetail
    form_class = EditStageInDetail
    template_name = 'workshop_data/product/product_add_detail.html'
    success_url = reverse_lazy('product_add_detail_complite')

    def get_object(self, **kwargs):
        obj = StageManufacturingDetail.objects.get(id=self.kwargs['pk'])
        return obj


#######################################################################################################


def product_create_complite(request):
    return render(request, 'workshop_data/worker/product_create_complite.html')


def detaile_create_complite(request):
    return render(request, 'workshop_data/detail/detail_create_complite.html')


def product_add_detail_complite(request):
    return render(request, 'workshop_data/product/product_add_detail_complite.html')


def product_add_in_plan_complite(request):
    return render(request, 'workshop_data/plan/product_add_in_plan.html')


def add_stage_in_detail_complite(request):
    return render(request, 'workshop_data/detail/stage/add_stage_in_detail_complite.html')


def new_batch_complite(request):
    return render(request, 'workshop_data/master/batch/new_batch_create_complite.html')


def start_new_stage_in_work_complite(request):
    return render(request, 'workshop_data/master/stage_in_work/start_new_stage_in_work_complete.html')


####################################         MASTER          ###########################################


class WorkerListView(LoginRequiredMixin, ListView):
    '''Отображает страницу всех работников(или выборка по специальности)'''
    model = User
    login_url = '/login/'
    template_name = 'workshop_data/master/workers_parametr_list.html'
    context_object_name = 'workers'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'LSM' in self.kwargs:
            context['workers'] = User.objects.filter(position='LSM')
        elif 'TRN' in self.kwargs:
            context['workers'] = User.objects.filter(position='TRN')
        else:
            context['workers'] = User.objects.filter(~Q(position='MSR'))
        print(self.kwargs)
        return context


class WorkerOrdersListForMaster(ListView):
    '''Показывает все наряды всех работников'''
    model = Order
    login_url = '/login/'
    template_name = 'workshop_data/worker/orders_user_parametr_list.html'  # шаблон из OrderUserParametrListView
    context_object_name = 'orders'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        if 'surname' in self.kwargs and 'month' not in self.kwargs:
            print('****surname')
            context['orders'] = Order.objects.filter(
                surname_id=User.objects.filter(
                    surname=self.kwargs['surname'], name=self.kwargs['name'])[0].id)
        elif 'month' in self.kwargs:
            print('****month')
            context['orders'] = Order.objects.filter(
                surname_id=User.objects.filter(
                    surname=self.kwargs['surname'], name=self.kwargs['name'])[0].id).filter(
                month=self.kwargs['month']
            )
            context['month'] = context['orders'][0]
        return context


class CreateBatchDetailInPlan(CreateView):
    '''Запуск в производсто новой партии Деталей'''
    model = BatchDetailInPlan
    form_class = CreateBatchDetailInPlanForm
    template_name = 'workshop_data/master/batch/create_batch_in_plan.html'
    success_url = reverse_lazy('product_add_plan_complite')

    def get_object(self, queryset=None):
        name = self.kwargs.pop('product')
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
        self.object.detail.in_work += self.object.quantity_in_batch
        self.object.detail.save()
        return HttpResponseRedirect(reverse_lazy('product_add_plan_complite'))


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
        # print('*****get_object*******')
        batch_id = self.kwargs.get('batch')
        obj = BatchDetailInPlan.objects.get(id=batch_id)
        return obj

    # def get_context_data(self, **kwargs):
    #     print('*****get_context_data*******')
    #     context = super().get_context_data(**kwargs)
    #     context['batch_id'] = self.get_object()
    #     return context

    def get_form_kwargs(self):
        print(StageManufacturingDetail.objects.filter(detail_id=self.get_object().detail.detail_id))
        kwargs = super(StageManufacturingDetailInWorkView, self).get_form_kwargs()
        kwargs.update({'batch': self.kwargs.get('batch')})
        kwargs.update(
            {'stages': StageManufacturingDetail.objects.filter(
                detail_id=self.get_object().detail.detail_id)}
        )
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('start_new_stage_in_work_complete'))


class AllBatchDetailInPlanView(ListView):
    '''Отображает все партии Деталей'''
    model = BatchDetailInPlan
    template_name = 'workshop_data/master/batch/all_batch_detail_in_plan.html'
    context_object_name = 'batchs_in_plan'
    ordering = ['detail']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
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
        print('****delete****')
        workshopplan_object = WorkshopPlan.objects.get(batchdetailinplan=self.kwargs.get('id'))
        batch = BatchDetailInPlan.objects.get(id=self.kwargs.get('id'))
        workshopplan_object.in_work -= batch.quantity_in_batch
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
        context['batchs_in_plan'] = BatchDetailInPlan.objects.filter(detail=self.get_object().id)
        return context


#######################    WorkshopPlan   ######################


class WorkshopPlanView(ListView):
    '''Отображает страницу План цеха'''
    model = WorkshopPlan
    template_name = 'workshop_data/plan/plan_list_all.html'
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_product'] = WorkshopPlan.objects.filter(month=current_month()).order_by('product')
        context['filter'] = WorkshopPlanFilter(self.request.GET, queryset=self.get_queryset().order_by('product'))
        return context


class WorkshopPlanCreateView(CreateView):
    '''Отображает страницу создания нового Плана'''
    model = WorkshopPlan
    form_class = WorkshopPlanCreateForm
    template_name = 'workshop_data/plan/plan_create.html'
    success_url = reverse_lazy('product_add_plan_complite')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class WorkshopPlanDeleteView(DeleteView):
    '''Удаление Детали из Плана'''
    model = WorkshopPlan
    template_name = 'workshop_data/plan/delete_object_from_workshopplan.html'
    success_url = reverse_lazy('plan', kwargs={'month': datetime.datetime.now().strftime('%b'),
                                               'year': datetime.datetime.now().strftime('%Y')})

    def get_object(self, queryset=None):
        dt = datetime.datetime.now()
        print(datetime.datetime.now().strftime('%b'))
        object = self.kwargs.pop('object')
        product = object.split('_')[0]
        detail = object.split('_')[1]
        obj = WorkshopPlan.objects.get(product__name=product, detail__name=detail)
        return obj
