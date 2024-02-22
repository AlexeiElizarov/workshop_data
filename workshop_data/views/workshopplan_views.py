import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView, ListView
from workshop_data.models.workshop_plan import WorkshopPlan
from workshop_data.forms import (
    WorkshopPlanCreateForm,
    EditWorkshopPlanForm,
    WorkshopPlanAddExistingBatchForm)
from ..filters import WorkshopPlanFilter
from ..models import BatchDetailInPlan, Product, Month, Comment


class WorkshopPlanView(LoginRequiredMixin, ListView):
    """Отображает страницу План цеха"""
    model = WorkshopPlan
    template_name = 'workshop_data/plan/plan_list_all.html'
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filter'] = WorkshopPlanFilter(
            self.request.GET,
            queryset=self.get_queryset().
            order_by('product', 'detail'))
        wps = context['filter'].qs.select_related('product', 'detail__prefix')
        products = Product.objects.filter(workshopplan__in=wps).distinct()
        context['products'] = products.prefetch_related(
            'detail',
            'detail__prefix',
            'detail__secondary_detail',

            )#'detail__in_warehouse'
        # self.request.session['month'] = self.request.GET['month']
        return context


class WorkshopPlanCreateView(LoginRequiredMixin, CreateView):
    """Отображает страницу создания новой Детали в Плане"""
    model = WorkshopPlan
    form_class = WorkshopPlanCreateForm
    template_name = 'workshop_data/plan/plan_create.html'
    success_url = reverse_lazy('product_add_plan_complete')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        super().form_valid(form)
        form.cleaned_data['comment'].workshop_plan = self.object
        form.cleaned_data['comment'].save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user._wrapped if hasattr(self.request.user,'_wrapped') else self.request.user
        return kwargs



class WorkshopPlanDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление Деталь из Плана"""
    model = WorkshopPlan
    template_name = 'workshop_data/plan/delete_object_from_workshopplan.html'
    success_url = reverse_lazy('plan', kwargs={'month': datetime.datetime.now().strftime('%b'),
                                               'year': datetime.datetime.now().strftime('%Y')})

    def get_object(self, queryset=None):
        # dt = datetime.datetime.now()
        object = self.kwargs.pop('object')
        product = object.split('_')[0]
        detail = object.split('_')[1]
        obj = WorkshopPlan.objects.get(product__name=product, detail__name=detail)
        return obj


class WorkshopPlanUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение Детали в Плане"""
    model = WorkshopPlan
    form_class = EditWorkshopPlanForm
    template_name = 'workshop_data/plan/plan_edit_detail.html'
    success_url = reverse_lazy('product_add_detail_complete') #FIXME

    def get_object(self, **kwargs):
        object = self.kwargs.get('object')
        product = object.split('_')[0]
        detail = object.split('_')[1]
        obj = WorkshopPlan.objects.get(product__name=product, detail__name=detail)
        return obj


class WorkshopPlanAddExistingBatchView(LoginRequiredMixin, UpdateView):
    """Страница добавления существующей партии в план"""
    model = WorkshopPlan
    form_class = WorkshopPlanAddExistingBatchForm
    template_name = 'workshop_data/plan/add_existing_batch_in_plan.html'

    def get_object(self, **kwargs):
        object = self.kwargs.get('object')
        product = object.split('_')[0]
        detail = object.split('_')[1].split('.')[1]
        obj = WorkshopPlan.objects.get(product__name=product, detail__name=detail)
        return obj

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = WorkshopPlanAddExistingBatchForm(request.POST)
            batch = BatchDetailInPlan.objects.get(id=form.data['batch'])
            batch.workshopplan_detail = self.get_object()
            batch.save()
            return HttpResponseRedirect(reverse_lazy('batchs_in_plan', kwargs={'object': self.get_object()}))
