import datetime

from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView, ListView
from workshop_data.models.workshop_plan import WorkshopPlan
from workshop_data.forms import WorkshopPlanCreateForm, EditWorkshopPlanForm
from ..filters import WorkshopPlanFilter
from workshop_data.services.general_services import current_month


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
    '''Отображает страницу создания новой Детали в Плане'''
    model = WorkshopPlan
    form_class = WorkshopPlanCreateForm
    template_name = 'workshop_data/plan/plan_create.html'
    success_url = reverse_lazy('product_add_plan_complite')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super().form_valid(form)


class WorkshopPlanDeleteView(DeleteView):
    '''Удаление Детали из Плана'''
    model = WorkshopPlan
    template_name = 'workshop_data/plan/delete_object_from_workshopplan.html'
    success_url = reverse_lazy('plan', kwargs={'month': datetime.datetime.now().strftime('%b'),
                                               'year': datetime.datetime.now().strftime('%Y')})

    def get_object(self, queryset=None):
        dt = datetime.datetime.now()
        object = self.kwargs.pop('object')
        product = object.split('_')[0]
        detail = object.split('_')[1]
        obj = WorkshopPlan.objects.get(product__name=product, detail__name=detail)
        return obj


class WorkshopPlanUpdateView(UpdateView):
    '''Изменение Детали в Плане'''
    model = WorkshopPlan
    form_class = EditWorkshopPlanForm
    template_name = 'workshop_data/plan/plan_edit_detail.html'
    success_url = reverse_lazy('product_add_detail_complite') #FIXME

    def get_object(self, **kwargs):
        object = self.kwargs.get('object')
        product = object.split('_')[0]
        detail = object.split('_')[1]
        obj = WorkshopPlan.objects.get(product__name=product, detail__name=detail)
        return obj
